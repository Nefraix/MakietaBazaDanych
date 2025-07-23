from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


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
