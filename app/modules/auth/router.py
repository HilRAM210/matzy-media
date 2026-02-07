from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth import schemas, services
from app.modules.users import schemas as user_schemas
from app.modules.users import services as user_services

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schemas.UserOut,
)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = user_services.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = user_services.create_user(db=db, user=user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = services.authenticate_user(
        db=db, email=user_credentials.username, password=user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = services.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
