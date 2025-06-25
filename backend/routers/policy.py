from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.policy import Policy
from backend.analyzer.insight_extractor import parse_ai_review
from backend.analyzer.rule_checker import rule_based_analysis
from backend.analyzer.compliance.comparator import PolicyComparator
from backend.analyzer.category_classifier import classify_policy_type
from backend.analyzer.industry_classifier import detect_industry
from backend.core.config import settings
from backend.models.auth import User
import uuid
import os
from typing import List
from backend.services.gemini import GeminiService # Ensure this import is present

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload-multiple")
async def upload_multiple_policies(files: List[UploadFile], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    uploaded_policies_info = []
    gemini_service = GeminiService() # Instantiate GeminiService

    for file in files:
        try:
            os.makedirs("uploads", exist_ok=True)
            
            file_path = f"uploads/{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            with open(file_path, "r", errors="ignore") as f:
                policy_text = f.read()
            
            policy_id = str(uuid.uuid4())
            
            # --- START of changed AI Review logic ---
            # Generate AI review using GeminiService directly
            ai_review_prompt = (
                "Provide a comprehensive review and key insights for the following policy text, "
                "focusing on its clarity, scope, and potential implications. "
                "Also, suggest categories and industry based on its content. "
                "Return the response in a structured JSON format with fields like 'review', 'insights', 'category', 'industry'. "
                "Example: {'review': '...', 'insights': '...', 'category': '...', 'industry': '...'}\n\n"
                f"Policy Text:\n{policy_text}"
            )
            ai_review_raw = await gemini_service.generate(ai_review_prompt)
            # Assuming parse_ai_review can handle the structured JSON string from ai_review_raw
            ai_review = parse_ai_review(ai_review_raw) 
            # --- END of changed AI Review logic ---

            rule_results = rule_based_analysis(policy_text) # This will need policy_text directly

            # Re-classify category and industry if parse_ai_review doesn't provide them,
            # or use values from ai_review if parse_ai_review extracts them
            category = ai_review.get("category", classify_policy_type(policy_text))
            industry = ai_review.get("industry", detect_industry(policy_text))

            policy = Policy(
                id=policy_id,
                filename=file.filename,
                ai_review=ai_review, # Ensure this matches your DB model's type (e.g., JSONB)
                insights=rule_results, # Ensure this matches your DB model's type (e.g., JSONB)
                category=category,
                industry=industry,
                user_id=user.id
            )
            
            db.add(policy)
            db.commit()
            db.refresh(policy)

            uploaded_policies_info.append({
                "message": f"Policy '{file.filename}' uploaded successfully",
                "policy_id": policy_id,
                "filename": file.filename
            })
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file '{file.filename}': {str(e)}"
            )
    
    return {"message": "Upload process completed", "uploaded_files": uploaded_policies_info}


@router.get("/enterprise/policies")
async def get_enterprise_policies(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    policies = db.query(Policy).filter(Policy.user_id == user.id).all()
    return policies


@router.get("/policy/{policy_id}")
async def get_policy(policy_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    policy = db.query(Policy).filter(Policy.id == policy_id, Policy.user_id == user.id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {
        "id": policy.id,
        "filename": policy.filename,
        "ai_review": policy.ai_review,
        "insights": policy.insights,
        "category": policy.category,
        "industry": policy.industry
    }

@router.post("/compare")
async def compare_policies(policy_id: str, gov_policy_text: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    policy = db.query(Policy).filter(Policy.id == policy_id, Policy.user_id == user.id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    comparator = PolicyComparator()
    # The 'raw' key might not exist if parse_ai_review doesn't create it,
    # or if ai_review is directly the parsed object.
    # It might be better to store the original policy_text in the DB if needed for comparison.
    comparison = comparator.compare_with_government(policy_text=policy.ai_review.get("raw", ""), gov_policy_text=gov_policy_text)
    return {"comparison": comparison}

# Global comparator instance (simplified for now)
comparator = PolicyComparator()