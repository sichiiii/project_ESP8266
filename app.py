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
        print(ip)
        ports = sql.get_ports(ip)
        print(ports)
        return {'ports':{'1':1, '2':0, '3':0, '4':0, '5':'-', '6':'-', '7':1, '8':1, '9':1, '10':1, '11':1, '12':'-', '13':1, '14':1, '15':1, '16':1}}    # TODO: Воззвращать состояние из базы
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/port_updates")
async def port_updates(request: Request):
    ports_json = request.json() 
    esp.update_ports(ports_json)

@esp8266.get("/check")
async def check(request: Request):
    try:
        status_json = {}
        statuses = esp.check()
        print(statuses)
        status_json[request.client.host] = json.loads(statuses)
        with open("test.txt", "a") as file:
            file.write(str(status_json)+'\n')
        return status_json
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/check")
async def check(request: Request):
    try:
        status_json = {}
        statuses = esp.check()
        print(statuses)
        status_json[request.client.host] = json.loads(statuses)
        with open("test.txt", "a") as file:
            file.write(str(status_json)+'\n')
        return status_json
    except Exception as ex:
        logger.error(str(ex))

@esp8266.get("/hardware")
async def hardware(request: Request):
    try:
        hardware = ['1', '2', '3', '4']
        return templates.TemplateResponse("hardware.html", {"request": request, "hardware" : hardware})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/hardware")
async def hardware(request: Request, url: str = Form(...)):
    try:
        return 'Building...'
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})


@esp8266.get("/home")
async def home(request: Request):
    try:
        data = esp.check()
        return templates.TemplateResponse("home.html", {"request": request, "data": data})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/home")
async def home(request: Request, url: str = Form(...)):
    try:
        return 'Building...'
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})