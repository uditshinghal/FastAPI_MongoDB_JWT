from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import users_collection
from app.models import User
from app.schemas import UserSchema, TokenSchema
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/signup", response_model=TokenSchema)
def signup(user: User):
    if users_collection.find_one({"e_email": user.e_email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    users_collection.insert_one(user_dict)

    access_token = create_access_token({"sub": user.e_email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return a JWT token"""
    user = users_collection.find_one({"e_email": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["e_email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserSchema])
def get_all_users(current_user: dict = Depends(get_current_user)):
    users = list(users_collection.find({}, {"password": 0}))
    return [UserSchema(**user) for user in users]

@router.delete("/users/{email}")
def delete_user(email: str, current_user: dict = Depends(get_current_user)):
    result = users_collection.delete_one({"e_email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
