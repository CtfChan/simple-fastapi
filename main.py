from typing import List
from typing_extensions import Annotated

import secrets

from models import Base, Lead
from schemas import LeadSchema, StateEnum
from database import engine,SessionLocal
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"user"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"123"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/addlead")
async def add_user(request:LeadSchema, db: Session = Depends(get_db)):
    lead = Lead(first_name=request.first_name, 
                last_name=request.last_name, 
                email=request.email, 
                resume_url=request.resume_url,
                state=StateEnum.pending)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@app.get("/leads", response_model=List[LeadSchema])
async def get_leads(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                    db: Session = Depends(get_db)):
    all_leads = db.query(Lead).all()
    return all_leads

@app.put("/lead/{lead_id}", response_model=LeadSchema)
async def update_lead(lead_update: LeadSchema, attorney_email: str, db: Session = Depends(get_db)):
    # Fetch lead in DB
    query = db.query(Lead).filter(Lead.id == lead_update.id)

    # Raise exception if lead not found
    lead = query.first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Send email to attorney and lead.
    # ...
    
    # Update DB.
    query.update(lead_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(lead)
    
    return lead_update

