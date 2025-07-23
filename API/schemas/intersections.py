from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


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