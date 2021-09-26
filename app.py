from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from pathlib import Path

import app_logger

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
async def root(request: Request):
    try:
        return 'Hello ESP8266, from Fastapi'
    except Exception as ex:
        logger.error(str(ex))