from pydantic import BaseModel, Field
from enum import Enum

class Decision(str, Enum):
    APPROVE = "APPROVE"
    DENY = "DENY"
    UNCERTAIN = "UNCERTAIN"

class GenericFile(BaseModel):
    filename: str
    content_type: str
    content: bytes

class ClaimSubmission(BaseModel):
    description: GenericFile = Field(..., description="The claim description file")
    supporting_docs: list[GenericFile] = Field([], description="List of supporting document files")

class ClaimProcessingResult(BaseModel):
    decision: Decision = Field(..., description="The status of the claim processing")
    explanation: str = Field(..., description="Reason for the status, if applicable")
    confidence: float = Field(..., description="Model confidence on the claim status choice, between 0 and 1", ge=0, le=1)

class TextExtraction(BaseModel):
    text: str = Field(description="The text extracted from the image")