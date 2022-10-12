from fastapi.responses import JSONResponse


def make_response(status, status_code, message, data=None):
    if data is None:
        return JSONResponse(status_code=status_code, content={
            'status': status,
            'message': message,
        })
    return JSONResponse(status_code=status_code, content={
        'status': status,
        'message': message,
        'data': data
    })
