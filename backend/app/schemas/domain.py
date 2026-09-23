from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Scene Schemas
class SceneResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    crs: Optional[str] = None
    bands: Optional[int] = None
    resolution: Optional[float] = None
    preprocessing_status: str
    uploaded_at: datetime
    bbox: Optional[List[float]] = None
    
    class Config:
        from_attributes = True
