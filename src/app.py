from fastapi import FastAPI
from api.router import upload
from utils.catch_exceptions import add_exception_handlers


class App:
    def __init__(self):
        self.app = FastAPI()
        self.include_routers()

    def start(self):
        add_exception_handlers(app=self.app)
        return self.app

    def include_routers(self):
        self.app.include_router(prefix='/api/v1', router=upload.router)


app = App().start()
