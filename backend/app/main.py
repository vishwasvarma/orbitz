from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.init_db import init_db
from app.routes import auth, users, activity, plans, progress

settings = get_settings()

app = FastAPI(title="Orbitz API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(activity.router)
app.include_router(plans.router)
app.include_router(progress.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"app": "Orbitz", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
