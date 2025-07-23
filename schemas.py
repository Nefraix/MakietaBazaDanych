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
    lights: int

" ---------- Pydantic Group ----------"

class GroupCreate(BaseModel):
    id: int
    description: Optional[str] = None

class GroupOut(GroupCreate):
    class Config:
        orm_mode = True
        
class GroupWithIQRF(BaseModel):
    id: int
    description: Optional[str] = None
    iqrf_devices: List[IQRFOut]  # 🔗 nested IQRF entries

    class Config:
        orm_mode = True

" ---------- Pydantic Intersection ----------"


class IntersectionOut(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class IntersectionWithIQRF(BaseModel):
    id: int
    name: str
    iqrf_devices: List[IQRFOut]

    class Config:
        orm_mode = True
        
        
class IntersectionCreate(BaseModel):
    id: int
    name:str
    class Config:
        orm_mode = True
        
class IntersectionWithIQRF(BaseModel):
    id: int
    name: str
    iqrf_devices: List[IQRFOut]

    class Config:
        orm_mode = True
        
        
class IntersectionWithMinimalIQRF(BaseModel):
    id: int
    name: str
    iqrf_devices: List[IQRFMinimal]

    class Config:
        orm_mode = True

" ---------- Pydantic Command ----------"

class CommandOut(BaseModel):
    id: int
    name: str
    code: str
    class Config:
        orm_mode = True
        
" ---------- Pydantic Situation ----------"

class SituationOut(BaseModel):
    id: int
    name: str
    code: Optional[str]

    class Config:
        orm_mode = True
        
