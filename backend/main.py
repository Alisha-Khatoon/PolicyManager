from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, policy
from backend.db.session import engine, init_db
from backend.core.config import settings  # Add this import

app = FastAPI()

# Initialize database
init_db()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth")  
app.include_router(policy.router, prefix="/api/policies")  

@app.get("/")
async def root():
    return {"message": "Policy Manager API"}