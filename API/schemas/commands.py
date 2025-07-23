from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


" ---------- Pydantic Command ----------"

class CommandOut(BaseModel):
    id: int
    name: str
    code: str
    class Config:
        orm_mode = True