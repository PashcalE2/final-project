class AppException(Exception):
    status_code: int

    def __init__(self, status_code: int, *args):
        super().__init__(*args)
        self.status_code = status_code
