from typing import List
from src.service import claim_analyser_run
from src.utils import parse_claim_submission
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/claims", tags=["claims"])

@router.post("/")
async def submit_claim(files: List[UploadFile] = File(...)):
    try:
        submission = await parse_claim_submission(files)
    except ValueError as e:
        return {"error": str(e)}

    claim_analyser_result = await claim_analyser_run(submission=submission)
    # print(claim_analyser_result.all_messages())
    return claim_analyser_result.output

@router.get("/{claim_id}")
async def get_claim_by_id(claim_id: str):
    return {"claim_id": claim_id, "status": "This endpoint is not yet implemented."}

@router.get("/")
async def get_claims():
    return {"claims": [], "status": "This endpoint is not yet implemented."}