from collections.abc import Sequence
from src.models import ClaimSubmission, GenericFile

class PromptsSequence(Sequence):
    def __init__(self, strings):
        self._strings = list(strings)  # Store as a list internally

    def __getitem__(self, index):
        return self._strings[index]  # Supports indexing and slicing

    def __len__(self):
        return len(self._strings)  # Required for len()

    def __repr__(self):
        return f"PromptsSequence({self._strings!r})"

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

async def save_claim():
    pass

async def retrieve_claims(id = None):
    if id:
        # Logi to load all claims in the system
        pass
    else:
        # Logic to load a specific claim
        pass