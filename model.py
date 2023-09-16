from typing import Optional
from pydantic import BaseModel, parse_obj_as
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///tasks.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


class TaskList(Base):
    __tablename__: str = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80))
    text = Column(Text, nullable=False)
    is_done = Column(Boolean, default=False)
    is_del = Column(Boolean, default=False)

    def __repr__(self):
        return f'id={self.id} title="{self.title}" text="{self.text}" is_done={self.is_done} is_del={self.is_del}'


class Task(BaseModel):
    title: Optional[str] = None
    text: str
    is_done: Optional[bool] = None
    is_del: Optional[bool] = None
