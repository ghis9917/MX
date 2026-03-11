from fastapi import FastAPI
from routers import claims
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ok"}

app.include_router(claims.router)