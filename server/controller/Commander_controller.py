from app.config import settings
from fastapi import APIRouter, status, Response
from server.consultas.commander_consulta import CommanderScraper

commander = APIRouter()


@commander.get(settings.API_V1 + "commander_of_day", status_code=status.HTTP_200_OK)
async def Commander_data():
    try:
        commander = CommanderScraper()
        return {"Commander": commander.commander_data()}
    except Exception as ex:
        print(ex)
        return Response(status_code=500)
