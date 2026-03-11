import os
import base64
from openai import OpenAI
from src.models import GenericFile, TextExtraction
from pydantic import BaseModel, Field

async def extract_text(image: GenericFile):
    base64_image = base64.b64encode(image.content).decode("utf-8")

    messages = [
        {"role": "system", "content": "You are an assistant that extracts text from images of any kind."},
        {"role": "user", "content": [
            {"type": "text", "text": "Extract the text from this image and translate it to english."},
            {"type": "image_url", "image_url": {"url": f"data:{image.content_type};base64,{base64_image}"}}
        ]}
    ]

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=TextExtraction
    )
    return response.choices[0].message.parsed.text