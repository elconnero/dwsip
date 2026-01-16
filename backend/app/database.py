import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

db = sa.create_engine("DATABASE_URL")
Session = sessionmaker(bind = db)
Base = declarative_base()