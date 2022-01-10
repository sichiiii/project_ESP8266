from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from fastapi.responses import FileResponse


import app_logger

from main import ESP
from pydantic import BaseModel
from pathlib import Path

import models, schemas, json
from database import SessionLocal, engine, SQL

models.Base.metadata.create_all(bind=engine)
sql = SQL()
esp = ESP()
logger = app_logger.get_logger(__name__)
esp8266 = FastAPI()

esp8266.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="templates")

directory=Path(__file__).parent.parent.absolute() 

@esp8266.get("/statuses")
async def index(request: Request):
    try:
        ip = request.client.host  
        is_exist = sql.check_new_ip(ip)
        if is_exist == True:
            ports = sql.get_ports(ip)
            print(ports)    #поменять это говнище внизу 
            return {'ports':{'1':ports[0][0], '2':ports[1][0], '3':ports[2][0], '4':ports[3][0],   
                '5':ports[4][0], '6':ports[5][0], '7':ports[6][0], '8':ports[7][0], '9':ports[8][0], 
                    '10':ports[9][0], '11':ports[10][0], '12':ports[11][0], '13':ports[12][0], 
                        '14':ports[13][0], '15':ports[14][0], '16':ports[15][0]}}   
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.get("/home")
async def home(request: Request):
    try:                                                                              
        data = sql.get_hardware()
        data_str = ''
        for i in range(len(data)):
            data_str += data[i][0] + ' '
        return templates.TemplateResponse("home.html", {"request": request, "data": data_str})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/select_instruct_hardware")
async def select_instruct_hardware(request: Request):
    try:                         
        data = sql.get_hardware()   
        data_str = ''
        for i in range(len(data)):
            data_str += data[i][0] + ' '                                                  
        return templates.TemplateResponse("select_instruct_hardware.html", {"request": request, "data": data})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/select_instruction")
async def create_instruction(request: Request):
    try:                 
        instructions = sql.get_instructions()
        instructions = [item[0] for item in instructions]
        print(instructions)
        return templates.TemplateResponse("select_instruction.html", {"request": request, "instructions": instructions})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.get("/create_instruction")
async def create_instruction(request: Request, ip: str, name: str):
    try:                 
        data = ip.split(',')
        return templates.TemplateResponse("create_instruction.html", {"request": request, "data": data, "name": name})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/set_ports")
async def set_ports(request: Request, hardware_select: str = Form(...)):
    try:
        ports = sql.get_ports(hardware_select)      #поменять это говнище внизу                           
        ports_json = {'ip':hardware_select, 'ports':{'1':ports[0][0], '2':ports[1][0], '3':ports[2][0], '4':ports[3][0], 
            '5':ports[4][0], '6':ports[5][0], '7':ports[6][0], '8':ports[7][0], '9':ports[8][0], '10':ports[9][0], 
                '11':ports[10][0], '12':ports[11][0], '13':ports[12][0], '14':ports[13][0], '15':ports[14][0], '16':ports[15][0]}}                                              
        return templates.TemplateResponse("set_ports.html", {"request": request, "ports":json.dumps(ports_json)})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/result")
async def result(request: Request):      
    try:
        req_info = await request.json()
        print(req_info)
        sql.update_ports(req_info['ip'], req_info['ports'])
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/select_instruction_result")
async def result(request: Request, insctruction_select: str = Form(...)):      
    try:
        sql.enable_instruction(insctruction_select)
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/result_insctruction")
async def result(request: Request):      
    try:
        req_info = await request.json()

        ip = req_info['ip']
        ports = req_info['ports']
        result_json = {}
        result_json['name'] = req_info['name']
        for i in range(0, len(ip)):
            result_json[ip[i]] = ports[16*(i):16*(i+1)]
        print(result_json)
        sql.insert_instruction(result_json)
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/export_instructions")
async def export_instructions(request: Request):
    try:
        sql.export_instructions()
        return FileResponse("instructions.csv")
    except Exception as ex:
        logger.error(str(ex))

@esp8266.get("/delete_all")
async def delete_all(request: Request):
    try:
        result = sql.delete_all()
        return result
    except Exception as ex:
        logger.error(str(ex))