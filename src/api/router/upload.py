from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse
from api.controller.upload import controller_uploader, handle_file
from starlette.background import BackgroundTasks
from core.app_error import AppError
from typing import Union

router = APIRouter(prefix='/video/upload')


@router.post('/', status_code=status.HTTP_200_OK)
async def upload_file(file: Union[UploadFile, None] = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    if file is None:
        raise AppError(message='Select a file',
                       status_code=status.HTTP_400_BAD_REQUEST)

    contents = await file.read()
    await file.close()

    is_valid = controller_uploader.is_valid_file(contents=contents)
    is_valid_size = controller_uploader.is_valid_size(contents=contents)

    if not is_valid:
        raise AppError(message='File format not allowed',
                       status_code=status.HTTP_400_BAD_REQUEST)
    elif not is_valid_size:
        raise AppError(message='File size must be less than 20Mb',
                       status_code=status.HTTP_400_BAD_REQUEST)

    file_info = await controller_uploader.save(filename=file.filename, contents=contents)

    upload_folder = file_info['upload_folder']
    out_folder = file_info['out_folder']
    filename = file_info['filename']
    file_path = file_info['file_path']
    key = file_info['key']

    zip_file_path, zip_file_name = await handle_file.split_video(key_uploaded_file=key, upload_folder=upload_folder, out_folder=out_folder,
                                                                 filename=filename, file_path=file_path)
    response = FileResponse(path=zip_file_path, filename=zip_file_name)
    background_tasks.add_task(controller_uploader.remove, upload_folder)
    return response
