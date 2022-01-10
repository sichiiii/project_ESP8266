from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

#from app import hardware
import app_logger, csv
import pandas as pd
from starlette.responses import FileResponse


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

    def get_hardware(self):
        hardware_table = Table('hardware', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(hardware_table.c.hardware)
                rs = con.execute(sthm)
                return rs.fetchall()
        except Exception as ex:
            self.logger.error(str(ex))

    def get_ports(self, ip):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==ip)
                hardware_ip = con.execute(sthm).fetchall()[0][0]
                sthm = select(ports_table.c.status).where(ports_table.c.hardware == hardware_ip)  
                rs = con.execute(sthm)                 
                return rs.fetchall()
        except Exception as ex:
            self.logger.error(str(ex))

    def get_instructions(self):
        instruction_table = Table('instruction', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(instruction_table.c.name).distinct()
                rs = con.execute(sthm)                 
                return rs.fetchall()
        except Exception as ex:
            self.logger.error(str(ex))

    def update_ports(self, ip, ports):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==ip)
                hardware_id = con.execute(sthm).fetchall()[0][0]
                for i in range(0, 16):
                    sthm = update(ports_table).where(and_(ports_table.c.hardware==hardware_id, ports_table.c.port==str(i+1))).values(status=int(ports[i]))
                    con.execute(sthm)
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

    def enable_instruction(self, name):
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        instruction_table = Table('instruction', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(instruction_table).where(instruction_table.c.name==name)
                instruction_arr = con.execute(sthm).fetchall()
                print(instruction_arr)
                for i in instruction_arr:
                    sthm = update(ports_table).where(and_(ports_table.c.hardware==i[4], ports_table.c.port==i[2])).values(status=i[3])
                    con.execute(sthm)
            return 'ok'
        except Exception as ex:
            self.logger.error(str(ex))

    def insert_instruction(self, instruction): #заменить айпи на айди айпишников
        hardware_table = Table('hardware', meta, autoload=True)
        ports_table = Table('ports', meta, autoload=True)
        instruction_table = Table('instruction', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(instruction_table.c.name).where(instruction_table.c.name==instruction['name'])
                res = con.execute(sthm).fetchall() 

                if res != []:
                    for i in range(1, len(instruction)):
                        sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==list(instruction)[i])
                        hardware_id = con.execute(sthm).fetchall()[0][0]
                        sthm = select(instruction_table.c.name).where(and_(instruction_table.c.name==instruction['name'], instruction_table.c.hardware==hardware_id))
                        hardware = con.execute(sthm).fetchall()

                        if hardware != []:
                            for j in range(0, 16):
                                sthm = update(instruction_table).where(and_(instruction_table.c.name==instruction['name'], instruction_table.c.hardware==hardware_id, instruction_table.c.port==str(j+1))).values(status=int(list(instruction.values())[i][j]))
                                con.execute(sthm)
                        else:
                            for j in range(0, 16):
                                sthm = insert(instruction_table).values(name=instruction['name'], hardware=hardware_id, port=str(j+1), status=int(list(instruction.values())[i][j]))
                                con.execute(sthm)
                else:
                    for i in range(1, len(instruction)):
                        sthm = select(hardware_table.c.id).where(hardware_table.c.hardware==list(instruction)[i])
                        hardware_id = con.execute(sthm).fetchall()[0][0]
                        for j in range(0, 16):
                            sthm = insert(instruction_table).values(name=instruction['name'], hardware=hardware_id, port=str(j+1), status=int(list(instruction.values())[i][j]))
                            con.execute(sthm)
                return {'status':'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}
        
    def export_instructions(self):
        try:
            with engine.connect() as con:  
                data = con.execute("SELECT * FROM instruction")
                print(data.fetchall())
                db_df = pd.read_sql_query("SELECT * FROM instruction", con)
                db_df.to_csv('instructions.csv', index=False)
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}

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
