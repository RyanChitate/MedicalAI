from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(name=patient.name)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=list[schemas.Patient])
def read_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

@app.post("/patients/{patient_id}/notes", response_model=schemas.Note)
def add_note(patient_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(patient_id=patient_id, **note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/patients/{patient_id}/notes", response_model=list[schemas.Note])
def get_notes(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Note).filter(models.Note.patient_id == patient_id).all()
