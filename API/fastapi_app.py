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
import logging
import time
import os

from API.schemas import *
from API.db import models, database
from API.routers import iqrf, commands, intersections, groups, situations


os.makedirs("logs", exist_ok=True)

log_file_path = "logs/logs.txt"

# Delete the log file if it exists
if os.path.exists(log_file_path):
    os.remove(log_file_path)


# Set up logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class LoggingMiddleware(BaseHTTPMiddleware):

    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            # Try reading the response body (requires capturing it first)
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            # Clone new response to preserve original output
            new_response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

            duration = time.time() - start_time
            msg = f"{request.method} {request.url.path} -> Status: {response.status_code} - Duration: {duration:.3f}s"

            # Try to extract error detail from response body
            if response.status_code >= 400:
                try:
                    body_data = json.loads(response_body)
                    if "detail" in body_data:
                        msg += f" - Detail: {body_data['detail']}"
                except Exception:
                    pass  # In case body isn't JSON

            logger.info(msg)
            return new_response

        except Exception as e:
            logger.error(f"Unhandled error in middleware: {e}")
            raise e



        
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

app.add_middleware(LoggingMiddleware)

app.include_router(iqrf.router)
app.include_router(intersections.router)
app.include_router(groups.router)
app.include_router(situations.router)
app.include_router(commands.router)

database.init_db()




# ---------- Root Endpoint ----------
"Used for getting all available endpoints"
@app.get("/")
async def root():
    return {
        "message": "Check 192.168.1.100/docs",
    }


 




# --- CONFIG---


@app.get("/config")
async def get_config():
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
