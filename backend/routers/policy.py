from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from typing import List
import os, json

from backend.utils.file_processing import extract_text_from_pdf, extract_text_from_docx
from backend.analyzer.rule_checker import rule_based_analysis
from backend.db.session import SessionLocal
from backend.schemas.policy import PolicyOut
from backend.models.policy import Policy

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Upload route with correct decorator and DB dependency
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type"}

    if not extracted_text:
        return {"error": "Failed to extract text from file"}

    # Analyze
    analysis_result = rule_based_analysis(extracted_text)

    # Save to DB
    new_policy = Policy(
        filename=file.filename,
        size=os.path.getsize(file_path),
        content=extracted_text,
        analysis=json.dumps(analysis_result),
    )
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return {
        "id": new_policy.id,
        "filename": new_policy.filename,
        "analysis": analysis_result,
        "preview_text": extracted_text[:1000]
    }

# ✅ Get all uploaded policies
@router.get("/", response_model=List[PolicyOut])
def get_all_policies(db: Session = Depends(get_db)):
    policies = db.query(Policy).order_by(Policy.uploaded_at.desc()).all()
    return policies
