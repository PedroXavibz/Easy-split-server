from fastapi import FastAPI, Request
from starlette import status
from core.app_error import AppError
from core.status_message import make_response


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exec: AppError):
        return make_response(status=exec.status, status_code=exec.status_code, message=exec.message)

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exec: Exception):
        print(exec)
        return make_response(status='error', message='Internal server error', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
