# backend/routers/policy.py

from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_policy(file: UploadFile = File(...)):
    content = await file.read()
    # Placeholder: We'll store this and run AI analysis later
    return {"filename": file.filename, "size": len(content)}
