from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
    UserOut,
    OnboardingRequest,
    ProfileUpdate,
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    username = payload.username.strip().lower()
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=username,
        password_hash=hash_password(payload.password),
        onboarding_complete=False,
    )
    db.add(user)
    db.commit()
    token = create_access_token(username)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = payload.username.strip().lower()
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(username))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/onboarding", response_model=UserOut)
def onboarding(
    payload: OnboardingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_goals = {"muscle_gain", "weight_gain", "weight_loss", "cardio", "general"}
    allowed_levels = {"beginner", "intermediate", "advanced"}
    if payload.fitness_goal not in allowed_goals:
        raise HTTPException(status_code=400, detail="Invalid fitness goal")
    if payload.fitness_level not in allowed_levels:
        raise HTTPException(status_code=400, detail="Invalid fitness level")

    current_user.name = payload.name
    current_user.age = payload.age
    current_user.gender = payload.gender
    current_user.height = payload.height
    current_user.weight = payload.weight
    current_user.fitness_goal = payload.fitness_goal
    current_user.fitness_level = payload.fitness_level
    current_user.onboarding_complete = True
    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/profile", response_model=UserOut)
def update_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user
