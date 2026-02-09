from fastapi import FastAPI

from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router
from app.modules.posts.router import router as post_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)


app.include_router(user_router, prefix=settings.app_prefix)
app.include_router(auth_router, prefix=settings.app_prefix)
app.include_router(post_router, prefix=settings.app_prefix)
