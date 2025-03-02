from pydantic import BaseModel, EmailStr
from typing import List

class AssetSchema(BaseModel):
    asset_id: str
    asset_desc: str
    asset_type: str
    asset_expiry: str

class UserSchema(BaseModel):
    e_name: str
    e_id: str
    e_email: EmailStr
    assets: List[AssetSchema]

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
