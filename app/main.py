from fastapi import FastAPI

from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(user_router)
app.include_router(auth_router)
