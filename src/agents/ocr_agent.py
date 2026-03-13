import os
import base64
from openai import OpenAI

from src.prompts import OCR_AGENT_PROMPT, OCR_TOOL_INNER_PROMPT
from src.constants import OCR_MODEL
from src.models import GenericFile, TextExtraction

async def extract_text(image: GenericFile):
    base64_image = base64.b64encode(image.content).decode("utf-8")

    messages = [
        {"role": "system", "content": OCR_AGENT_PROMPT},
        {"role": "user", "content": [
            {"type": "text", "text": OCR_TOOL_INNER_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:{image.content_type};base64,{base64_image}"}}
        ]}
    ]

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.beta.chat.completions.parse(
        model=OCR_MODEL,
        messages=messages,
        response_format=TextExtraction
    )
    return response.choices[0].message.parsed.text