from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


   
" ---------- Pydantic Situation ----------"

class SituationOut(BaseModel):
    id: int
    name: str
    code: Optional[str]

    class Config:
        orm_mode = True
        