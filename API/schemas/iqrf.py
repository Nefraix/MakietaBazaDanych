from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

" ---------- Pydantic IQRF ----------"

class IQRFCreate(BaseModel):
    id: int
    group: int
    intersection: Optional[int] = 5
    priority: Optional[int] = 0
    lights: Optional[int] = 0
    description: Optional[str] = None
    
class IQRFOut(BaseModel):
    id: int
    group: int
    intersection: int
    priority: Optional[int] = 5
    lights: Optional[int] = 0
    description: Optional[str] = None
    class Config:
        orm_mode = True

# This schema excludes `description`
class IQRFMinimal(BaseModel):
    id: int
    group: int
    intersection: int
    priority: int
    lights: int

    class Config:
        orm_mode = True
        
class IQRFUpdateLED(BaseModel):
    id: int
    lights: int  # adjust type depending on your schema (e.g., List[str] or JSON)
