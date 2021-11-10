from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(Integer, primary_key=True, index=True)
    hardware = Column(String)
    ports = relationship("Item", back_populates="port_parent")

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    port = Column(String, index=True)
    status = Column(Integer)
    hardware = Column(Integer, ForeignKey("hardware.id"))

