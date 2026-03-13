import os
import json
import uuid
from typing import Dict, List

from src.constants import STORAGE_PATH, CHOICE_FILENAME
from src.models import ClaimSubmission, ClaimProcessingResult, GenericFile


async def parse_claim_submission(files) -> ClaimSubmission:
    description = None
    supporting_docs = []

    for file in files:
        if file.filename == "description.txt":
            description = file
        else:
            supporting_docs.append(file)
            
    if description is None:
        raise ValueError("Missing 'description.txt' file in the submission.")
    
    return await prepare_claim_submission(description, supporting_docs)

async def prepare_claim_submission(description, supporting_docs) -> ClaimSubmission:
    return ClaimSubmission(
        description=GenericFile(
            filename=description.filename,
            content_type=description.content_type,
            content=await description.read()
        ),
        supporting_docs=[
            GenericFile(
                filename=doc.filename,
                content_type=doc.content_type,
                content=await doc.read()
            ) for doc in supporting_docs
        ]
    )

async def save_claim(submission: ClaimSubmission, result: ClaimProcessingResult) -> Dict | None:

    uuid_str = str(uuid.uuid4())
    claim_path = os.path.join(STORAGE_PATH, f"claim_{uuid_str}")
    os.makedirs(claim_path)

    description = os.path.join(claim_path, submission.description.filename)
    with open(description, "wb") as f:
        f.write(submission.description.content)

    for doc in submission.supporting_docs:
        doc_path = os.path.join(claim_path, doc.filename)
        with open(doc_path, "wb") as f:
            f.write(doc.content)

    result_path = os.path.join(claim_path, CHOICE_FILENAME)
    with open(result_path, "w") as f:
        json.dump(result, f, indent=4)

    return uuid_str



async def retrieve_claims(id = None) -> List[Dict] | Dict:
    if id is None:
        claims = []
        for claim_folder in os.listdir(STORAGE_PATH):
            claim_path = os.path.join(STORAGE_PATH, claim_folder)
            if os.path.isdir(claim_path):
                file_path = os.path.join(claim_path, CHOICE_FILENAME)
                with open(file_path, 'r') as f:
                    result = json.load(f)
                claims.append({
                    'id': claim_folder.split('_')[1],
                    'result': result
                })
        return claims
    else:
        claim_path = os.path.join(STORAGE_PATH, f"claim_{id}")
        if os.path.isdir(claim_path):
            file_path = os.path.join(claim_path, CHOICE_FILENAME)
            with open(file_path, 'r') as f:
                result = json.load(f)
            return {
                'id': id, 
                'result': result
            }