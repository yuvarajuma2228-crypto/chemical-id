from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class CHEMICAL(Base):
    __tablename__ = "chemicals"

    sno = Column(Integer, primary_key=True)
    name = Column(String)
    formula = Column(String)
    mw = Column(Float)
    bp = Column(Float)