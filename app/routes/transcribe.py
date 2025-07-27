from fastapi import APIRouter, UploadFile, File
from app.nlp.pipeline import process_audio

router = APIRouter()

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    result = process_audio(file)
    return {"data": result}
