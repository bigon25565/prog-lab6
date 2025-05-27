from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Union, Dict

from models import Base, TermModel
from database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Term(BaseModel):
    description: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/terms")
def get_all_terms(db: Session = Depends(get_db)):
    terms = db.query(TermModel).all()
    return {term.keyword: {"description": term.description} for term in terms}

@app.get("/terms/{term}")
def get_term(term: str, db: Session = Depends(get_db)):
    db_term = db.query(TermModel).filter(TermModel.keyword == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return {db_term.keyword: {"description": db_term.description}}

@app.post("/terms/{term}")
def post_term(term: str, term_data: Term, db: Session = Depends(get_db)):
    existing = db.query(TermModel).filter(TermModel.keyword == term).first()
    if existing:
        raise HTTPException(status_code=400, detail="Term already exists!")
    new_term = TermModel(keyword=term, description=term_data.description)
    db.add(new_term)
    db.commit()
    return {term: term_data}

@app.put("/terms/{term}")
def change_term(term: str, term_data: Term, db: Session = Depends(get_db)):
    existing = db.query(TermModel).filter(TermModel.keyword == term).first()
    if not existing:
        raise HTTPException(status_code=400, detail="Term not found!")
    existing.description = term_data.description
    db.commit()
    return {term: term_data}

@app.delete("/terms/{term}")
def delete_term(term: str, db: Session = Depends(get_db)):
    db_term = db.query(TermModel).filter(TermModel.keyword == term).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found!")
    db.delete(db_term)
    db.commit()
    return {"result": "deleted successfully"}

@app.get("/author")
def read_about():
    from datetime import datetime
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    except locale.Error:
        pass  # fallback if locale not available in container
    return {'author': "Nick", "datetime": datetime.now().strftime("%A, %d.%m.%Y, %H:%M").title()}
