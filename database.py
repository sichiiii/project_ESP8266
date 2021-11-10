from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

from app import hardware
import app_logger
from sqlalchemy import select

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData(engine)
Base = declarative_base()

class SQL():
    def __init__(self):
        self.logger = app_logger.get_logger(__name__)

    def get_ports(self, ip):
        hardware = Table('hardware', meta, autoload=True)
        ports = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select([ports]).where(ports.hardware == ip)
                rs = con.execute(sthm)
                return rs
        except Exception as ex:
            self.logger.error(str(ex))

    def update_ports(self, ports):
        hardware = Table('hardware', meta, autoload=True)
        ports = Table('ports', meta, autoload=True)
        try:
            pass
        except Exception as ex:
            self.logger.error(str(ex))