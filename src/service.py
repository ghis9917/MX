from pydantic_ai import Agent, RunContext, BinaryContent
from src.models import ClaimProcessingResult, ClaimSubmission, GenericFile
from typing import List
from src.utils import PromptsSequence
from src.prompts import *
import base64

claim_analyser = Agent(
    'openai:gpt-5.4',
    deps_type=ClaimSubmission,
    output_type=ClaimProcessingResult,
    retries=3,
    system_prompt=PromptsSequence([
        MAIN_AGENT_PROMPT,
        DESCRIPTION_ANALYSER_TOOL_PROMPT,
        FRAUD_CHECKER_TOOL_PROMPT,
        SUPPORTING_DOCS_ANALYSER_TOOL_PROMPT
    ])
)

@claim_analyser.system_prompt
async def add_policy_info(ctx: RunContext[ClaimSubmission]) -> str:
    with open('./data/policy.md', 'r') as file:
        policy = file.read()
    return f"The policy to use as a reference for your decision making is the following: {policy}"

fraud_checker = Agent(
    'openai:gpt-4o',
    output_type=str,
    retries=3,
    system_prompt=FRAUD_CHECKER_AGENT_PROMPT
)

@claim_analyser.tool
async def check_document_validity(ctx: RunContext[ClaimSubmission]) -> List[str]:
    docs = ctx.deps.supporting_docs

    results = []
    for doc in docs:
        result = await fraud_checker.run(
            [
                FRAUD_CHECK_ANALYSER_TOOL_INNER_PROMPT,
                BinaryContent(data=doc.content, media_type=doc.content_type)
            ]
        )
        results.append(f"Assessment for {doc.filename}: {result.output}")

    return results

file_analyser = Agent(
    'openai:gpt-4o',
    output_type=str,
    retries=3,
    system_prompt=FILE_ANALYSER_AGENT_PROMPT
)

@claim_analyser.tool
async def analyse_description(ctx: RunContext[ClaimSubmission]) -> str:
    description = ctx.deps.description

    result = await file_analyser.run(
        [
            DESCRIPTION_ANALYSER_TOOL_INNER_PROMPT,
            BinaryContent(data=description.content, media_type=description.content_type)
        ]
    )
    return f"Description: {result.output}"

@claim_analyser.tool
async def analyse_supporting_docs(ctx: RunContext[ClaimSubmission]) -> List[str]:
    docs = ctx.deps.supporting_docs

    results = []
    for doc in docs:
        result = await file_analyser.run(
            [
                SUPPORTING_DOCS_ANALYSER_TOOL_INNER_PROMPT,
                BinaryContent(data=doc.content, media_type=doc.content_type)
            ]
        )
        results.append(f"Assessment for {doc.filename}: {result.output}")

    return results

async def claim_analyser_run(submission: ClaimSubmission) -> ClaimProcessingResult:
    return await claim_analyser.run("Analyze the claim submission.", deps=submission)