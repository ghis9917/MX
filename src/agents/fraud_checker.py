from typing import List
from pydantic_ai import Agent, BinaryContent

from src.models import GenericFile
from src.prompts import (
    FRAUD_CHECKER_AGENT_PROMPT,
    FRAUD_CHECK_ANALYSER_TOOL_INNER_PROMPT
)

fraud_checker = Agent(
    'openai:gpt-4o',
    output_type=str,
    retries=3,
    system_prompt=FRAUD_CHECKER_AGENT_PROMPT
)

async def supporting_docs_fraud_check(docs: List[GenericFile]) -> List[str]:
    results = []
    for doc in docs:
        result = await fraud_checker.run(
            [
                FRAUD_CHECK_ANALYSER_TOOL_INNER_PROMPT,
                BinaryContent(data=doc.content, media_type=doc.content_type)
            ],
        )
        results.append(f"Assessment for {doc.filename}: {result.output}")

    return results