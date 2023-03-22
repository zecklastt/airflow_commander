from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = "/api/"
    PROJECT_NAME: str = "commander_of_day"


settings = Settings()
