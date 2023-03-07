from fastapi import FastAPI
from server.controller.Commander_controller import commander


app = FastAPI(
    title="BUSCANDO O COMANDANTE DO DIA COM APACHE AIRFLOW",
)
app.include_router(commander)