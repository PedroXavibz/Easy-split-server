from fastapi import FastAPI


class App:
    def __ini__(self):
        self.app = FastAPI()

    def start(self):
        return self.app


app = App().start()
