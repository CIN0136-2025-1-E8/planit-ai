from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from sqlalchemy.orm import Session

from app.crud import get_user_crud
from app.dependencies import get_db
from app.models import User

token_scheme = HTTPBearer()


async def get_current_user(
        db: Session = Depends(get_db),
        user_crud=Depends(get_user_crud),
        token: HTTPAuthorizationCredentials = Depends(token_scheme)
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required"
        )

    try:
        decoded_token = auth.verify_id_token(token.credentials)
        firebase_uid = decoded_token['uid']
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    db_user = user_crud.get(db=db, obj_uuid=firebase_uid)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User profile not found. Please complete registration."
        )

    return db_user
