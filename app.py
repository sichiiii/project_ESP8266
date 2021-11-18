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
        ports = sql.get_ports(ip)
        sql.check_new_ip(ip)
        print(ports)
        return {'ports':{'1':1, '2':0, '3':0, '4':0, '5':'-', '6':'-', '7':1, '8':1, '9':1, '10':1, '11':1, '12':'-', '13':1, '14':1, '15':1, '16':1}}    # TODO: Воззвращать состояние из базы
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.post("/port_updates")
async def port_updates(request: Request):
    ports_json = request.json() 
    esp.update_ports(ports_json)

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

@esp8266.get("/delete_all")
async def delete_all(request: Request):
    try:
        result = sql.delete_all()
        return result
    except Exception as ex:
        logger.error(str(ex))