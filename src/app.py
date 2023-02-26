from fastapi import FastAPI
from api.router import upload
from utils.catch_exceptions import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from core.config import Config


class App:
    def __init__(self):
        self.app = FastAPI()
        self.include_middlewares()
        self.include_routers()

    def start(self):
        add_exception_handlers(app=self.app)
        return self.app

    def include_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[Config.ORIGIN],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def include_routers(self):
        self.app.include_router(prefix='/api/v1', router=upload.router)


app = App().start()
