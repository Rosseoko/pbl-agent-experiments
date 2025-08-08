from fastapi import FastAPI
from app.pbl_assistant.controller import router

app = FastAPI(title="AI PBL Assistant")
app.include_router(router)

