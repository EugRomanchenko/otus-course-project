from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)
