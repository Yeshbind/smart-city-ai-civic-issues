from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import issues, engineer
from db import engine, Base
import models
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart City Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(issues.router, prefix="/api")
app.include_router(engineer.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Smart City Backend Running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
