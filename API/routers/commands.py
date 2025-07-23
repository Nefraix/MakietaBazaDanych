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
    tags=["commands"],
    responses={404: {"description": "Not found"}},
)


# ---------- Command Endpoints ----------

@router.get("/get_all_commands", response_model=List[CommandOut], tags=["commands"])
def get_all_commands():
    db: Session = SessionLocal()
    commands = db.query(Command).all()
    db.close()
    return commands
    
@router.get("/get_command_byID/{command_id}", response_model=CommandOut, tags=["commands"])
def get_command_by_id(command_id: int):
    db: Session = SessionLocal()
    command = db.query(Command).filter(Command.id == command_id).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    return situation

