
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.v1.auth.repository import UserRepository
from app.core.db import get_db
from app.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    oauth2_token,
    require_admin,
    verify_password,
)
from app.models.user import User

from .schemas import RoleUpdate, TokenResponse, UserCreate, UserLogin, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)

    if repository.get_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado"
        )

    try:
        user = repository.create_user(
            email=payload.email,
            fullname=payload.full_name,
            hashed_password=hash_password(payload.password),
        )

        db.commit()
        db.refresh(user)

        return UserPublic.model_validate(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear usuario"
        )


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: Session = Depends(get_db)):
    repository = UserRepository(db)

    user = repository.get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    token = create_access_token(sub=str(user.id))

    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.put("/role/{user_id}", response_model=UserPublic)
def set_role(
    user_id: int = Path(ge=1),
    payload: RoleUpdate = None,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    repository = UserRepository(db)
    user = repository.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    try:
        updated_user = repository.set_role(user=user, role=payload.role)

        db.commit()
        db.refresh(updated_user)

        return UserPublic.model_validate(updated_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el rol"
        )


@router.post("/token")
async def token_endpoint(response=Depends(oauth2_token)):
    return response


@router.get("/me", response_model=UserPublic)
async def read_me(current: User = Depends(get_current_user)):
    return UserPublic.model_validate(current)
