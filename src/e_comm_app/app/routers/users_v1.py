from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from e_comm_app.app.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from e_comm_app.app.config import get_db
from e_comm_app.app.models.user_models import PasswordChangeRequest, UserCreate, TokenRequest
from e_comm_app.app.orm.e_comm_orm import User

router = APIRouter(
    prefix="/users", tags=["user-auth"], responses={404: {"description": "Not found"}}
)


@router.post("/get_token")
def login_for_access_token(
    token_request: TokenRequest, db: Session = Depends(get_db)
):
    user = authenticate_user(db, token_request.username, token_request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": f"Bearer {access_token}"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Hash the password and create the user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username, hashed_password=hashed_password, email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User successfully registered"}


@router.put(
    "/change-password", status_code=status.HTTP_200_OK, summary="Change Password"
)
async def change_password(
    password_data: PasswordChangeRequest,
    db: Session = Depends(get_db),
):
    # Fetch the user by username
    current_user = (
        db.query(User).filter(User.username == password_data.username).first()
    )

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    # Verify current password
    if not verify_password(
        password_data.current_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )

    # Hash and update the new password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()

    return {"message": "Password changed successfully"}
