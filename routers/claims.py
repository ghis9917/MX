from typing import List
from src.agents.claim_analyser import claim_analyser_run
from src.utils import parse_claim_submission, retrieve_claims, save_claim
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/claims")

@router.post("/")
async def submit_claim(files: List[UploadFile] = File(...)):
    try:
        submission = await parse_claim_submission(files)
        claim_analyser_result = await claim_analyser_run(submission=submission)
        uuid = await save_claim(submission, claim_analyser_result.output.dict())
    except Exception as e:
        return {'error': str(e)}
    
    return {'id': uuid, 'result': claim_analyser_result.output}

@router.get("/{claim_id}")
async def get_claim_by_id(claim_id: str):
    try:
        claim = await retrieve_claims(claim_id)
    except Exception as e:
        return {'error': str(e)}
    return claim

@router.get("/")
async def get_claims():
    try:
        claims = await retrieve_claims()
    except Exception as e:
        return {'error': str(e)}
    return claims