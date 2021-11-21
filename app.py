from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

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
            print(ports)
            return {'ports':{'1':ports[0][0], '2':ports[1][0], '3':ports[2][0], '4':ports[3][0], \
                '5':ports[4][0], '6':ports[5][0], '7':ports[6][0], '8':ports[7][0], '9':ports[8][0], \
                    '10':ports[9][0], '11':ports[10][0], '12':ports[11][0], '13':ports[12][0], \
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

@esp8266.post("/set_ports")
async def set_ports(request: Request, hardware_select: str = Form(...)):
    try:
        ports = sql.get_ports(hardware_select)                              
        ports_json = {'ip':hardware_select, 'ports':{'1':ports[0][0], '2':ports[1][0], '3':ports[2][0], '4':ports[3][0], \
            '5':ports[4][0], '6':ports[5][0], '7':ports[6][0], '8':ports[7][0], '9':ports[8][0], '10':ports[9][0], \
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
        return 'ok'
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.get("/delete_all")
async def delete_all(request: Request):
    try:
        result = sql.delete_all()
        return result
    except Exception as ex:
        logger.error(str(ex))