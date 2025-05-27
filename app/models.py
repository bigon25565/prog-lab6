from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TermModel(Base):
    __tablename__ = 'terms'
    keyword = Column(String, primary_key=True, index=True)
    description = Column(String)
