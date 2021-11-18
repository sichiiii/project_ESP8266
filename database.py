from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

#from app import hardware
import app_logger


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
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==ip)
                hardware_ip = con.execute(sthm).fetchall()[0][0]
                sthm = select(ports_table.c.status).where(ports_table.c.hardware == hardware_ip)  #получение всех статусов и отправление в джс для установки стаусов на страничке
                rs = con.execute(sthm)                 
                return rs.fetchall()
        except Exception as ex:
            self.logger.error(str(ex))

    def update_ports(self, ip, ports):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = update(ports_table).where(ports_table.c.hardware == ip)
            pass  
        except Exception as ex:
            self.logger.error(str(ex))

    def check_new_ip(self, ip):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = exists(hardware_table).select().where(hardware_table.c.hardware == ip)
                rs = con.execute(sthm).fetchall()
                if rs == []:
                    sthm = insert(hardware_table).values(hardware=ip)
                    con.execute(sthm)
                    sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==ip)
                    hardware_id = con.execute(sthm).fetchall()[0][0]
                    for i in range(1, 17):
                        sthm = insert(ports_table).values(port=str(i), status=0, hardware=hardware_id)
                        con.execute(sthm) 
                return rs[0][0]
        except Exception as ex:
            self.logger.error(str(ex))

    def delete_all(self):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = delete(hardware_table)
                con.execute(sthm)
                sthm = delete(ports_table)
                con.execute(sthm)
                return {'status':'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}
