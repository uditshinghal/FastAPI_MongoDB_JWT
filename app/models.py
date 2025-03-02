from pydantic import BaseModel, EmailStr
from typing import List

class Asset(BaseModel):
    asset_id: str
    asset_desc: str
    asset_type: str
    asset_expiry: str

class User(BaseModel):
    e_name: str
    e_id: str
    e_email: EmailStr
    assets: List[Asset]
    password: str
