from app.database.connection import Base, engine
from app.models import user, activity, analysis, plan  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
