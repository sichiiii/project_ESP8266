from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from main import ESP
from pydantic import BaseModel
from pathlib import Path

import app_logger, json

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

@esp8266.get("/")
async def index(request: Request):
    try:
        print(request.client.host)  # IP ---> Database
        return {'ports':{'1':0, '2':1, '3':1}}
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

@esp8266.get("/check")
async def check(request: Request):
    try:
        status_json = {}
        status_json[request.client.host] = esp.check()
        with open("test.txt", "a") as file:
            file.write(str(status_json)+'\n')
        return status_json
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})

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
        final_url = urlCheckerObject.get_url()
        return templates.TemplateResponse("watch.html", {"request": request, "url" : final_url})
    except Exception as ex:
        logger.error(str(ex))
        return templates.TemplateResponse("error.html", {"request": request})