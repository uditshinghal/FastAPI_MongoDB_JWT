from fastapi import FastAPI
from app.routes import users, assets

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])

