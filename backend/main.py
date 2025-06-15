# backend/main.py

from fastapi import FastAPI
from routers import policy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(policy.router, prefix="/api/policies", tags=["Policy"])

@app.get("/")
def root():
    return {"message": "Enterprise Policy Manager API is running"}
