import logging

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance.init_logger()
        return cls._instance

    def init_logger(self):
        if hasattr(self, "logger") and self.logger.handlers:
            return

        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.DEBUG)

        log_format = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)

        file_handler = logging.FileHandler("file_explorer.log")
        file_handler.setFormatter(log_format)

        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.ERROR)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger