from fastapi import FastAPI

from .internal import admin
from .routers import users

app = FastAPI()

app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello sir, I'm under the water."}
