from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    height: float | None = None
    weight: float | None = None
    fitness_goal: str | None = None
    fitness_level: str | None = None
    onboarding_complete: bool

    class Config:
        from_attributes = True


class OnboardingRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    age: int = Field(ge=10, le=100)
    gender: str
    height: float = Field(gt=50, lt=300)
    weight: float = Field(gt=20, lt=400)
    fitness_goal: str
    fitness_level: str


class ProfileUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    height: float | None = None
    weight: float | None = None
    fitness_goal: str | None = None
    fitness_level: str | None = None
