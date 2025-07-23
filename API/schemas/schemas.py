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
        
" --------- Pydantic Tag -------------------"
class TagCreate(BaseModel):
    """
    Pydantic model for creating a new Tag entry.
    UUID is expected to be provided by the client as it's the primary key.
    Intersection and priority are optional, with default values.
    Code is required, and description is optional.
    """
    uuid: str  # Assuming UUID is provided by the client or generated before this schema is used
    intersection: Optional[int] = None
    priority: Optional[int] = 0
    code: str
    description: Optional[str] = None

    class Config:
        # Allows ORM models to be used directly with Pydantic
        orm_mode = True

class TagRead(BaseModel):
    """
    Pydantic model for reading (response) Tag entries.
    Includes all fields from the Tag model.
    """
    uuid: str
    intersection: Optional[int] = None
    priority: Optional[int] = None # When reading, default from DB will be present
    code: str
    description: Optional[str] = None

    class Config:
        # Allows ORM models to be used directly with Pydantic
        orm_mode = True

class TagLightState(BaseModel):
    intersection_id: int
    priority: int
    lights_value: int

    class Config:
        orm_mode = True
