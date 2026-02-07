from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.modules.users import schemas, services
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db=db, user_id=id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )
    return user
