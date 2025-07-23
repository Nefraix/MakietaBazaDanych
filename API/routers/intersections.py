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
    tags=["intersections"],
    responses={404: {"description": "Not found"}},
)


# ---------- Intersection Endpoints ----------
@router.post("/post_intersection", response_model=IntersectionOut, tags=["intersections"])
def create_intersection(intersection: IntersectionCreate):
    db: Session = SessionLocal()
    db_intersection = Intersection(id=intersection.id, name=intersection.name)
    db.add(db_intersection)
    db.commit()
    db.refresh(db_intersection)
    db.close()
    return db_intersection


@router.get("/get_all_intersections", response_model=List[IntersectionOut], tags=["intersections"])
def get_all_intersections():
    db: Session = SessionLocal()
    intersections = db.query(Intersection).all()
    db.close()
    return intersections

@router.get("/get_intersection_byID/{intersection_id}", response_model=IntersectionWithIQRF, tags=["intersections"])
def get_intersection_by_id(intersection_id: int):
    db: Session = SessionLocal()
    
    # Get the intersection
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        db.close()
        raise HTTPException(status_code=404, detail="Intersection not found")
    
    # Get related IQRF devices
    iqrf_list = db.query(IQRF).filter(IQRF.intersection == intersection_id).all()
    
    db.close()
    
    return {
        "id": intersection.id,
        "name": intersection.name,
        "iqrf_devices": iqrf_list
    }
    
    
@router.get("/get_intersection_with_lights_byID/{intersection_id}", response_model=IntersectionWithMinimalIQRF, tags=["intersections"])
def get_intersection_with_lights_by_id(intersection_id: int):
    db: Session = SessionLocal()
    
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        db.close()
        raise HTTPException(status_code=404, detail="Intersection not found")

    iqrf_list = db.query(IQRF).filter(IQRF.intersection == intersection_id).all()

    db.close()

    return {
        "id": intersection.id,
        "name": intersection.name,
        "iqrf_devices": iqrf_list
    }

@router.delete("/delete_intersection_byID/{intersection_id}", tags=["intersections"])
def delete_intersection(intersection_id: int):
    db: Session = SessionLocal()
    intersection = db.query(Intersection).filter(Intersection.id == intersection_id).first()
    if not intersection:
        db.close()
        raise HTTPException(status_code=404, detail="Intersection not found")
    db.delete(intersection)
    db.commit()
    db.close()
    return {"message": f"Intersection with id {intersection_id} deleted"}


