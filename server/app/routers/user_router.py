from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.user import user_crud
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserData

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post("/", response_model=UserData)
def create_user(
        name: str = Form(),
        nickname: str | None = Form(None),
        email: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db),
):
    user_in: UserCreate = UserCreate(
        name=name,
        nickname=nickname,
        email=email,
        password=password,
    )
    db_user = user_crud.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = user_crud.create(db=db, obj_in=user_in)
    return user


@user_router.get("/", response_model=UserData)
def get_user(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user = user_crud.get(db, obj_uuid=user.uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@user_router.put("/", response_model=UserData)
def update_user(
        new_name: str | None = Form(None),
        new_nickname: str | None = Form(None),
        new_email: str | None = Form(None),
        new_password: str | None = Form(None),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_new_data: UserUpdate = UserUpdate(
        name=new_name,
        nickname=new_nickname,
        email=new_email,
        password=new_password,
    )
    db_user = user_crud.get(db, obj_uuid=user.uuid)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = user_crud.update(db=db, db_obj=db_user, obj_in=user_new_data)
    return updated_user


@user_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user = user_crud.remove(db, obj_uuid=user.uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return
