from pydantic_ai import Agent, RunContext
from typing import List

from src.prompts import *
from src.constants import CLAIM_ANALYSER_MODEL
from src.agents.file_analyser import *
from src.agents.fraud_checker import *
from src.models import ClaimProcessingResult, ClaimSubmission

claim_analyser = Agent(
    CLAIM_ANALYSER_MODEL,
    deps_type=ClaimSubmission,
    output_type=ClaimProcessingResult,
    retries=3,
    system_prompt=[
        MAIN_AGENT_PROMPT,
        DESCRIPTION_ANALYSER_TOOL_PROMPT,
        FRAUD_CHECKER_TOOL_PROMPT,
        SUPPORTING_DOCS_ANALYSER_TOOL_PROMPT
    ]
)

@claim_analyser.system_prompt
async def add_policy_info(ctx: RunContext[ClaimSubmission]) -> str:
    with open('./data/policy.md', 'r') as file:
        policy = file.read()
    return f"The policy to use as a reference for your decision making is the following: {policy}"

@claim_analyser.tool
async def check_document_validity(ctx: RunContext[ClaimSubmission]) -> List[str]:
    docs = ctx.deps.supporting_docs
    return await supporting_docs_fraud_check(docs)

@claim_analyser.tool
async def analyse_description(ctx: RunContext[ClaimSubmission]) -> str:
    description = ctx.deps.description
    return await description_analysis(description)

@claim_analyser.tool
async def analyse_supporting_docs(ctx: RunContext[ClaimSubmission]) -> List[str]:
    docs = ctx.deps.supporting_docs
    return await supporting_docs_analysis(docs)

async def claim_analyser_run(submission: ClaimSubmission) -> ClaimProcessingResult:
    return await claim_analyser.run("Analyze the claim submission.", deps=submission)