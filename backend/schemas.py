from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    date: datetime
    model_config = {
    "from_attributes": True
}

class PatientBase(BaseModel):
    name: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    notes: list[Note] = []
    model_config = {
    "from_attributes": True
}