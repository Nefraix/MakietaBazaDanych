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
    tags=["groups"],
    responses={404: {"description": "Not found"}},
)

# ---------- Group Endpoints ----------


@router.post("/post_group", response_model=GroupOut, tags=["groups"])
def create_group(group: GroupCreate):
    db = SessionLocal()
    db_group = Group(id=group.id, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    db.close()
    return db_group

@router.get("/get_all_groups", response_model=List[GroupOut], tags=["groups"])
def read_groups():
    db = SessionLocal()
    groups = db.query(Group).all()
    db.close()
    return groups

@router.get("/get_group_byID/{group_id}", response_model=GroupWithIQRF, tags=["groups"])
def read_group_by_id(group_id: int):
    db = SessionLocal()
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        db.close()
        raise HTTPException(status_code=404, detail="Group not found")

    # 🔎 Query related IQRF records
    iqrf_list = db.query(IQRF).filter(IQRF.group == group_id).all()

    db.close()

    return {
        "id": group.id,
        "description": group.description,
        "iqrf_devices": iqrf_list
    }
    
@router.delete("/delete_group_byID/{group_id}", tags=["groups"])
def delete_group(group_id: int):
    db = SessionLocal()
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        db.close()
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    db.close()
    return {"message": f"Group with id {group_id} deleted"}
    
    
