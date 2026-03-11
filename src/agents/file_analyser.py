from typing import List
from pydantic_ai import Agent, BinaryContent

from src.agents.ocr_agent import extract_text
from src.prompts import (
    FILE_ANALYSER_AGENT_PROMPT,
    DESCRIPTION_ANALYSER_TOOL_INNER_PROMPT, 
    SUPPORTING_DOCS_ANALYSER_TOOL_INNER_PROMPT
)

file_analyser = Agent(
    'openai:gpt-4o',
    output_type=str,
    retries=3,
    system_prompt=FILE_ANALYSER_AGENT_PROMPT
)

async def description_analysis(description) -> str:

    result = await file_analyser.run(
        [
            DESCRIPTION_ANALYSER_TOOL_INNER_PROMPT,
            BinaryContent(data=description.content, media_type=description.content_type)
        ]
    )
    return f"Description: {result.output}"

async def supporting_docs_analysis(docs) -> List[str]:

    results = []
    for doc in docs:

        content = BinaryContent(data=doc.content, media_type=doc.content_type)
        
        if doc.content_type.startswith('image'): # If it's an image, extract the text first and analyse that instead
            text = await extract_text(doc)
            content = BinaryContent(data=text.encode('utf-8'), media_type='text/plain')

        result = await file_analyser.run(
            [
                SUPPORTING_DOCS_ANALYSER_TOOL_INNER_PROMPT,
                content
            ]
        )
        results.append(f"Assessment for {doc.filename}: {result.output}")

    return results