from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

from models import Base, IQRF, Group, Situation, Command, Intersection
from schemas import *
from database import SessionLocal, init_db

tags_metadata = [
    {
        "name": "iqrf",
        "description": "Individual IQRF nodes",
    },
    {
        "name": "intersections",
        "description": "individual intersections",
    },
    {
        "name": "groups",
        "description": "Groups of IQRFs",
    },
    {
        "name": "commands",
        "description": "commands that the car reads after scanning appropiate RFID tag",
    },
    {
        "name": "situations",
        "description": "Road situations with HEX codes",
    },

]


app = FastAPI(
    title="Smart Traffic Control API",
    description="API for managing smart traffic infrastructure using IQRF communication technology.",
    version="1.0.0",
    openapi_tags=tags_metadata)



init_db()




# ---------- Root Endpoint ----------
"Used for getting all available endpoints"
@app.get("/")
def root():
    return {
        "message": "Available endpoints and table schemas:",
        "routes": {
            "IQRF": {
                "GET all": "/iqrf",
                "GET by ID": "/iqrf/{id}",
                "POST": "/iqrf",
                "DELETE": "/iqrf/{id}"
            },
            "Groups": {
                "GET all": "/groups",
                "GET by ID": "/groups/{id}",
                "POST": "/groups",
                "DELETE": "/groups/{id}"
            },
            "Commands": {
                "GET all": "/commands",
                "GET by ID": "/commands/{id}"
            },
            "Situations": {
                "GET all": "/situations",
                "GET by ID": "/situations/{id}",
                "GET by Code": "/situations/by_code/{code}"
            },
            "Intersections": {
                "GET all": "/intersections",
                "GET by ID": "/intersections/{id}",
                "POST": "/intersections",
                "DELETE": "/intersections/{id}"
            },
            "Config": {
                "GET": "/config"
            }
        },
        "schemas": {
            "iqrf": ["id", "group (groups.id)","intersection (intersections.id)", "priority", "lights", "description"],
            "groups": ["id", "description"],
            "commands": ["id", "name", "code"],
            "situations": ["id", "name", "code"],
            "intersections": ["id", "name"]
        },
        "example_requests": {
            "IQRF": {
                "GET all": "curl -X GET http://192.168.1.100:8040/iqrf",
                "GET by ID": "curl -X GET http://192.168.1.100:8040/iqrf/1",
                "POST": "curl -X POST http://192.168.1.100:8040/iqrf -H \"Content-Type: application/json\" -d '{\"id\": 1, \"group\": 1, \"intersection\": 5, \"priority\": 0, \"lights\": 0, \"description\": \"Example IQRF\"}'",
                "DELETE": "curl -X DELETE http://192.168.1.100:8040/iqrf/1"
            },
            "Groups": {
                "GET all": "curl -X GET http://192.168.1.100:8040/groups",
                "GET by ID": "curl -X GET http://192.168.1.100:8040/groups/1",
                "POST": "curl -X POST http://192.168.1.100:8040/groups -H \"Content-Type: application/json\" -d '{\"id\": 1, \"description\": \"Example Group\"}'",
                "DELETE": "curl -X DELETE http://192.168.1.100:8040/groups/1"
            },
            "Commands": {
                "GET all": "curl -X GET http://192.168.1.100:8040/commands",
                "GET by ID": "curl -X GET http://192.168.1.100:8040/commands/1"
            },
            "Situations": {
                "GET all": "curl -X GET http://192.168.1.100:8040/situations",
                "GET by ID": "curl -X GET http://192.168.1.100:8040/situations/1",
                "GET by Code": "curl -X GET http://192.168.1.100:8040/situations/by_code/0001"
            },
            "Intersections": {
                "GET all": "curl -X GET http://192.168.1.100:8040/intersections",
                "GET by ID": "curl -X GET http://192.168.1.100:8040/intersections/1",
                "POST": "curl -X POST http://192.168.1.100:8040/intersections -H \"Content-Type: application/json\" -d '{\"id\": 1, \"name\": \"Main Street\"}'",
                "DELETE": "curl -X DELETE http://192.168.1.100:8040/intersections/1"
            },
            "Config": {
                "GET": "curl -X GET http://192.168.1.100:8040/config"
            }
        }
    }


 
# ---------- IQRF Endpoints ----------

@app.post("/post_iqrf_overwriting", response_model=IQRFOut, tags=["iqrf"])
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

@app.post("/post_iqrf", response_model=IQRFOut, tags=["iqrf"])
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

@app.get("/get_all_iqrfs", response_model=List[IQRFOut], tags=["iqrf"])
def read_iqrf():
    db = SessionLocal()
    iqrf_list = db.query(IQRF).all()
    db.close()
    return iqrf_list

@app.get("/get_iqrf_byID/{iqrf_id}", response_model=IQRFOut, tags=["iqrf"])
def read_iqrf_by_id(iqrf_id: int):
    db = SessionLocal()
    iqrf = db.query(IQRF).filter(IQRF.id == iqrf_id).first()
    db.close()
    if iqrf is None:
        raise HTTPException(status_code=404, detail="IQRF record not found")
    return iqrf
    
@app.delete("/delete_iqrf_byID/{iqrf_id}", tags=["iqrf"])
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
    
    
# ---------- Group Endpoints ----------


@app.post("/post_group", response_model=GroupOut, tags=["groups"])
def create_group(group: GroupCreate):
    db = SessionLocal()
    db_group = Group(id=group.id, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    db.close()
    return db_group

@app.get("/get_all_groups", response_model=List[GroupOut], tags=["groups"])
def read_groups():
    db = SessionLocal()
    groups = db.query(Group).all()
    db.close()
    return groups

@app.get("/get_group_byID/{group_id}", response_model=GroupWithIQRF, tags=["groups"])
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
    
@app.delete("/delete_group_byID/{group_id}", tags=["groups"])
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
    
    
# ---------- Command Endpoints ----------

@app.get("/get_all_commands", response_model=List[CommandOut], tags=["commands"])
def get_all_commands():
    db: Session = SessionLocal()
    commands = db.query(Command).all()
    db.close()
    return commands
    
@app.get("/get_command_byID/{command_id}", response_model=CommandOut, tags=["commands"])
def get_command_by_id(command_id: int):
    db: Session = SessionLocal()
    command = db.query(Command).filter(Command.id == command_id).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    return situation


# ---------- Situation Endpoints ----------


@app.get("/get_all_situations", response_model=List[SituationOut], tags=["situations"])
def get_all_situations():
    db: Session = SessionLocal()
    situations = db.query(Situation).all()
    db.close()
    return situations
    
@app.get("/get_situation_byID/{situation_id}", response_model=SituationOut, tags=["situations"])
def get_situation_by_id(situation_id: int):
    db: Session = SessionLocal()
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    return situation
    
@app.get("/get_situation_byCODE/{code}", response_model=SituationOut, tags=["situations"])
def get_situation_by_code(code: str):
    db: Session = SessionLocal()
    situation = db.query(Situation).filter(Situation.code == code).first()
    db.close()
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found for given code")
    return situation


# ---------- Intersection Endpoints ----------
@app.post("/post_intersection", response_model=IntersectionOut, tags=["intersections"])
def create_intersection(intersection: IntersectionCreate):
    db: Session = SessionLocal()
    db_intersection = Intersection(id=intersection.id, name=intersection.name)
    db.add(db_intersection)
    db.commit()
    db.refresh(db_intersection)
    db.close()
    return db_intersection


@app.get("/get_all_intersections", response_model=List[IntersectionOut], tags=["intersections"])
def get_all_intersections():
    db: Session = SessionLocal()
    intersections = db.query(Intersection).all()
    db.close()
    return intersections

@app.get("/get_intersection_byID/{intersection_id}", response_model=IntersectionWithIQRF, tags=["intersections"])
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
    
    
@app.get("/get_intersection_with_lights_byID/{intersection_id}", response_model=IntersectionWithMinimalIQRF, tags=["intersections"])
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

@app.delete("/delete_intersection_byID/{intersection_id}", tags=["intersections"])
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


# --- CONFIG---


@app.get("/config")
def get_config():
    db: Session = SessionLocal()

    # Get all intersections
    intersections = db.query(Intersection).all()

    # Map each intersection with related IQRFs
    intersections_with_iqrf = []
    for intersection in intersections:
        related_iqrf = db.query(IQRF).filter(IQRF.intersection == intersection.id).all()
        intersections_with_iqrf.append({
            "id": intersection.id,
            "name": intersection.name,
            "iqrf_devices": related_iqrf
        })

    # Get all IQRFs
    all_iqrf = db.query(IQRF).all()

    db.close()

    return {
        "intersections": intersections_with_iqrf,
        "all_iqrf": all_iqrf
    }


# --- Exception handler --- 


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig)

    if "FOREIGN KEY constraint failed" in error_message:
        return JSONResponse(
            status_code=400,
            content={"detail": "Cannot create or delete: Foreign Key constraint violation."},
        )

    if "UNIQUE constraint failed" in error_message or "duplicate key value violates unique constraint" in error_message:
        return JSONResponse(
            status_code=400,
            content={"detail": "Duplicate ID or unique field value. The record already exists."},
        )

    return JSONResponse(
        status_code=500,
        content={"detail": f"Database integrity error: {error_message}"},
    )