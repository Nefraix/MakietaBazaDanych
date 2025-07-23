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

from API.database import models, database
from API.schemas import *

from FastAPI import APIRouter, Depends, HTTPException


router = APIRouter(
    tags=["iqrf"],
    responses={404: {"description": "Not found"}},
)

# ---------- IQRF Endpoints ----------

@router.post("/post_iqrf_overwriting", response_model=IQRFOut, tags=["iqrf"])
def create_or_overwrite_iqrf(iqrf: IQRFCreate):
    db = SessionLocal()
    try:
        existing_iqrf = db.query(IQRF).filter(IQRF.id == iqrf.id).first()

        # Delete any other IQRF with same intersection and priority
        conflicting = db.query(IQRF).filter(
            IQRF.intersection == iqrf.intersection,
            IQRF.priority == iqrf.priority,
            IQRF.id != iqrf.id
        ).first()
        if conflicting:
            db.delete(conflicting)

        if existing_iqrf:
            existing_iqrf.group = iqrf.group
            existing_iqrf.intersection = iqrf.intersection
            existing_iqrf.priority = iqrf.priority
            existing_iqrf.lights = iqrf.lights
            existing_iqrf.description = iqrf.description
        else:
            existing_iqrf = IQRF(
                id=iqrf.id,
                group=iqrf.group,
                intersection=iqrf.intersection,
                priority=iqrf.priority,
                lights=iqrf.lights,
                description=iqrf.description
            )
            db.add(existing_iqrf)

        db.commit()
        db.refresh(existing_iqrf)
        return existing_iqrf

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Foreign key constraint failed. Ensure group and intersection exist.")

    finally:
        db.close()

@router.post("/post_iqrf", response_model=IQRFOut, tags=["iqrf"])
def create_iqrf(iqrf: IQRFCreate):
    db = SessionLocal()
    
    # Delete any existing IQRF with the same intersection and priority (but different ID)
    conflicting = db.query(IQRF).filter(
        IQRF.intersection == iqrf.intersection,
        IQRF.priority == iqrf.priority,
        IQRF.id != iqrf.id
    ).first()
    if conflicting:
        db.delete(conflicting)

    db_iqrf = IQRF(
        id=iqrf.id,
        group=iqrf.group,
        intersection=iqrf.intersection,
        priority=iqrf.priority,
        lights=iqrf.lights,
        description=iqrf.description
    )
    db.add(db_iqrf)
    db.commit()
    db.refresh(db_iqrf)
    db.close()
    return db_iqrf

@router.post("/post_iqrf_change_led", tags=["iqrf"])
def post_iqrf_change_led(update: IQRFUpdateLED):
    db =SessionLocal()
    iqrf = db.query(IQRF).filter(IQRF.id == update.id).first()
    if not iqrf:
        raise HTTPException(status_code=404, detail="IQRF device not found")

    iqrf.lights = update.lights
    db.commit()
    db.refresh(iqrf)

@router.get("/get_all_iqrfs", response_model=List[IQRFOut], tags=["iqrf"])
def read_iqrf():
    db = SessionLocal()
    iqrf_list = db.query(IQRF).all()
    db.close()
    return iqrf_list

@router.get("/get_iqrf_byID/{iqrf_id}", response_model=IQRFOut, tags=["iqrf"])
def read_iqrf_by_id(iqrf_id: int):
    db = SessionLocal()
    iqrf = db.query(IQRF).filter(IQRF.id == iqrf_id).first()
    db.close()
    if iqrf is None:
        raise HTTPException(status_code=404, detail="IQRF record not found")
    return iqrf

@router.get("/get_iqrf_LED_byID/{iqrf_id}", response_model=IQRFUpdateLED, tags=["iqrf"])
def read_iqrf_by_id(iqrf_id: int):
    db = SessionLocal()
    iqrf = db.query(IQRF).filter(IQRF.id == iqrf_id).first()
    db.close()
    if iqrf is None:
        raise HTTPException(status_code=404, detail="IQRF record not found")
    return IQRFUpdateLED(id=iqrf.id, lights=iqrf.lights)
    
@router.delete("/delete_iqrf_byID/{iqrf_id}", tags=["iqrf"])
def delete_iqrf(iqrf_id: int):
    db = SessionLocal()
    iqrf_item = db.query(IQRF).filter(IQRF.id == iqrf_id).first()
    if not iqrf_item:
        db.close()
        raise HTTPException(status_code=404, detail="IQRF item not found")
    db.delete(iqrf_item)
    db.commit()
    db.close()
    return {"message": f"IQRF item with id {iqrf_id} deleted"}
    
    