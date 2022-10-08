from fastapi import FastAPI
from db.base import DataBase


class App:
    def __init__(self):
        self.app = FastAPI()

    def start(self):
        return self.app


app = App().start()


@app.on_event('startup')
async def startup_db_client():
    DataBase.connect()


@app.on_event('shutdown')
async def shutdown_db_client():
    DataBase.close()
