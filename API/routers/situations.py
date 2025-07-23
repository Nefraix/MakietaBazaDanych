from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from API.db import models, database
from API.schemas import *

from FastAPI import APIRouter, Depends, HTTPException

router = APIRouter(
    tags=["situations"],
    responses={404: {"description": "Not found"}},
)

# ---------- Situation Endpoints ----------


@router.get("/get_all_situations", response_model=List[SituationOut], tags=["situations"])
def get_all_situations():
    db: Session = SessionLocal()
    situations = db.query(Situation).all()
    db.close()
    return situations
    
@router.get("/get_situation_byID/{situation_id}", response_model=SituationOut, tags=["situations"])
def get_situation_by_id(situation_id: int):
    db: Session = SessionLocal()
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    return situation
    
@router.get("/get_situation_byCODE/{code}", response_model=SituationOut, tags=["situations"])
def get_situation_by_code(code: str):
    db: Session = SessionLocal()
    situation = db.query(Situation).filter(Situation.code == code).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found for given code")
    return situation
