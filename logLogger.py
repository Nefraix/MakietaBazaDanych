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


log_file_path = "logs/logs.txt"


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