from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    manga_type = Column(String)  # US / JP
    status = Column(String, default="uploaded")
