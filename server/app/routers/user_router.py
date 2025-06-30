from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.dependencies import get_db
from app.crud.user import user_crud
from app.schemas.user_schema import UserCreate, UserUpdate, User

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = user_crud.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = user_crud.create(db=db, obj_in=user_in)
    return user

@user_router.get("/", response_model=list[User])
def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users

@user_router.get("/{user_uuid}", response_model=User)
def read_user_by_uuid(
    user_uuid: str,
    db: Session = Depends(get_db)
):
    user = user_crud.get(db, obj_uuid=user_uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@user_router.put("/{user_uuid}", response_model=User)
def update_existing_user(
    user_uuid: str, 
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = user_crud.get(db, obj_uuid=user_uuid)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = user_crud.update(db=db, db_obj=db_user, obj_in=user_update)
    return updated_user

@user_router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(
    user_uuid: str,
    db: Session = Depends(get_db)
):
    user = user_crud.remove(db, obj_uuid=user_uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
