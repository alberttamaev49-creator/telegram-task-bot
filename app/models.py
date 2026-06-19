from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False)