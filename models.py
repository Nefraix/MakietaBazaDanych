from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()



    
class IQRF(Base):
    __tablename__ = "iqrf"
    id = Column(Integer, primary_key=True, index=False)
    group = Column(Integer, ForeignKey("groups.id"), nullable=False, default=0)
    intersection = Column(Integer, ForeignKey("intersections.id"), nullable=False,default=5)
    priority = Column(Integer, nullable=False, default=0) 
    lights = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=True)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    
class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)

class Situation(Base):
    __tablename__ = "situations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    
class Intersection(Base):
    __tablename__ = "intersections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
