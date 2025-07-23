
     
" --------- Pydantic Tag -------------------"
class TagCreate(BaseModel):
    """
    Pydantic model for creating a new Tag entry.
    UUID is expected to be provided by the client as it's the primary key.
    Intersection and priority are optional, with default values.
    Code is required, and description is optional.
    """
    uuid: str  # Assuming UUID is provided by the client or generated before this schema is used
    intersection: Optional[int] = None
    priority: Optional[int] = 0
    code: str
    description: Optional[str] = None

    class Config:
        # Allows ORM models to be used directly with Pydantic
        orm_mode = True

class TagRead(BaseModel):
    """
    Pydantic model for reading (response) Tag entries.
    Includes all fields from the Tag model.
    """
    uuid: str
    intersection: Optional[int] = None
    priority: Optional[int] = None # When reading, default from DB will be present
    code: str
    description: Optional[str] = None

    class Config:
        # Allows ORM models to be used directly with Pydantic
        orm_mode = True

class TagLightState(BaseModel):
    intersection_id: int
    priority: int
    lights_value: int

    class Config:
        orm_mode = True
