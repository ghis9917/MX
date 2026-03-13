from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import claims # do not move before load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ok"}

app.include_router(claims.router)