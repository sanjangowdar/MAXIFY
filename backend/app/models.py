from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True,nullable=False)
    password_hash:Mapped[str]=mapped_column(String(255),nullable=False)
    role:Mapped[str]=mapped_column(String(30),default="user",nullable=False)
    created_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class Profile(Base):
    __tablename__="profiles"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id:Mapped[int]=mapped_column(Integer,index=True,unique=True)
    display_name:Mapped[str]=mapped_column(String(100),default="")
    data_json:Mapped[str]=mapped_column(String(10000),default="{}")
