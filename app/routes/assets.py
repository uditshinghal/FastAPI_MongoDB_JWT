from fastapi import APIRouter, Depends
from app.database import users_collection
from app.models import Asset
from app.schemas import AssetSchema
from app.auth import get_current_user

router = APIRouter()

@router.post("/assets", response_model=AssetSchema)
def add_asset(asset: Asset, current_user: dict = Depends(get_current_user)):
    users_collection.update_one({"e_email": current_user["e_email"]}, {"$push": {"assets": asset.dict()}})
    return asset

@router.get("/assets", response_model=list[AssetSchema])
def get_assets(current_user: dict = Depends(get_current_user)):
    return current_user.get("assets", [])

@router.delete("/assets/{asset_id}")
def delete_asset(asset_id: str, current_user: dict = Depends(get_current_user)):
    users_collection.update_one({"e_email": current_user["e_email"]}, {"$pull": {"assets": {"asset_id": asset_id}}})
    return {"message": "Asset deleted"}
