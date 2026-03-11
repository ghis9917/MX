from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ok"}

# do not move before load_dotenv()
from routers import claims 

app.include_router(claims.router)