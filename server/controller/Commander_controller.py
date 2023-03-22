from app.config import settings
from datetime import datetime
import pytz

from fastapi import APIRouter, status, Response
from server.consultas.commander_consulta import CommanderScraper

commander = APIRouter()


@commander.get(settings.API_V1 + "commander_of_day", status_code=status.HTTP_200_OK)
async def Commander_data():
    try:
        commander = CommanderScraper()
        name, url = commander.commander_data()
        return {"name": name,
                "url": url,
                "date": datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M'),
                }
    except Exception as ex:
        print(ex)
        return Response(status_code=500)
