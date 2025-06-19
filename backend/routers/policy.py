from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os, json

from backend.utils.file_processing import extract_text_from_pdf, extract_text_from_docx
from backend.analyzer.rule_checker import rule_based_analysis
from backend.analyzer.gemini_checker import ai_compliance_check
from backend.db.session import SessionLocal
from backend.schemas.policy import PolicyOut, PolicyDetailOut
from backend.models.policy import Policy

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Upload route
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from supported formats
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == "docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type"}

    if not extracted_text:
        return {"error": "Failed to extract text from file"}

    # Run analyses
    analysis_result = rule_based_analysis(extracted_text)
    ai_review = ai_compliance_check(extracted_text)

    # Save to database
    new_policy = Policy(
        filename=file.filename,
        size=os.path.getsize(file_path),
        content=extracted_text,
        analysis=json.dumps(analysis_result),
        ai_review=ai_review,
    )
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return {
        "filename": new_policy.filename,
        "size": new_policy.size,
        "analysis": analysis_result,
        "ai_review": ai_review,
        "preview_text": extracted_text[:1000]
    }


# ✅ Get all policies
@router.get("/", response_model=List[PolicyOut])
def get_all_policies(db: Session = Depends(get_db)):
    return db.query(Policy).order_by(Policy.uploaded_at.desc()).all()


# ✅ Get single policy details
@router.get("/{policy_id}", response_model=PolicyDetailOut)
def get_policy_by_id(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    return {
        "id": policy.id,
        "filename": policy.filename,
        "size": policy.size,
        "uploaded_at": policy.uploaded_at,
        "content": policy.content,
        "analysis": json.loads(policy.analysis),
        "ai_review": policy.ai_review,
    }
