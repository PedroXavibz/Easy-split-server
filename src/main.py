import uvicorn
from core.config import Config

if __name__ == '__main__':
    uvicorn.run(app='app:app', host=Config.HOST,
                port=Config.PORT, log_level=Config.LOG_LEVEL, debug=Config.DEBUG, reload=Config.RELOAD)
