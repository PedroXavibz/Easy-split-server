class AppError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message: str = message
        self.status_code: int = status_code
        self.status: str = 'fail' if str(
            self.status_code).startswith('4') else 'error'
        self.is_operational = True
        super().__init__(self.message)
