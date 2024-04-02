import logging
import subprocess
import uuid
from typing import Any, List, Optional, Tuple

from fastapi import Request

command = ["git", "status", "-s"]

result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

awk_command = ["awk", "{print $2}"]
awk_input = result.stdout  # Convert the output to bytes for awk

awk_result = subprocess.run(
    awk_command, input=awk_input, stdout=subprocess.PIPE, text=True
)

git_status = awk_result.stdout.split("\n")


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;32m"
    grey = "\x1b[34;34m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = """%(levelname)s - %(asctime)s - %(message)s
    - %(name)s - %(url_path)s - %(file_name)s"""

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LogFiles:
    paths_git_status: List[str] = []
    paths_inserted: List[str] = []

    def __init__(self, paths_git_status: List[str]):
        self.paths_git_status = paths_git_status
        self.paths_inserted = []

    def paths(self):
        return [*self.paths_git_status, *self.paths_inserted]


class RequestLogger:
    logger: logging.LoggerAdapter
    buffer: List[Tuple[Any]]
    log_files: LogFiles
    file_name: str
    url_path: str
    child: Optional["RequestLogger"] = None
    parent: Optional["RequestLogger"] = None

    def __init__(
        self,
        logger,
        url_path: str,
        log_files: LogFiles,
        file_name: str,
        parent: Optional["RequestLogger"] = None,
        buffer=None,
    ):
        self.buffer = buffer if buffer else []
        self.url_path = url_path
        self.logger = logger
        self.parent = parent
        self.log_files = log_files
        self.file_name = file_name

    def debug(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.error(msg, *args, **kwargs)
        else:
            self.buffer.append((logging.DEBUG, msg, args, kwargs))

    def warning(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(logging.WARNING):
            self.logger.error(msg, *args, **kwargs)
        else:
            self.buffer.append((logging.WARNING, msg, args, kwargs))

    def info(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(msg, *args, **kwargs)
        else:
            self.buffer.append((logging.INFO, msg, args, kwargs))

    def error(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(logging.ERROR):
            self.logger.error(msg, *args, **kwargs)
        else:
            self.buffer.append((logging.ERROR, msg, args, kwargs))

    def exception(self, msg, *args, **kwargs):
        self.flush()
        self.logger.exception(msg, *args, **kwargs)

    def getChild(self, suffix: str, file: str):
        logger = self.logger.logger.getChild(suffix)
        adapter = self.__make_adapter__(logger, file)
        request_logger = RequestLogger(
            logger=adapter,
            url_path=self.url_path,
            parent=self,
            file_name=file,
            log_files=self.log_files,
            buffer=[],
        )
        self.child = request_logger
        return request_logger

    def flush(self):
        if self.parent is not None:
            return self.parent.flush()
        for lvl, msg, args, kwargs in self.buffer:
            if self.logger.process is not None:
                msg, kwargs = self.logger.process(msg, kwargs)
            self.logger._log(lvl, msg, args, **kwargs)
        self.buffer.clear()
        if self.child is not None:
            self.child.parent = None
            self.child.flush()

    def __make_adapter__(self, logger: logging.Logger, file: str):
        return logging.LoggerAdapter(
            logger=logger, extra={"url_path": self.url_path, "file_name": file}
        )


def create_logger():
    logger = logging.getLogger("API")
    logger.setLevel(logging.ERROR)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger


def create_request_logger(req: Request):
    request_id = str(uuid.uuid4())
    logger: logging.Logger = req.app.state.logger.getChild(request_id)
    logger.getChild(request_id)
    logger = logging.LoggerAdapter(
        logger=logger,
        extra={
            "url_path": req.url.path,
            "file_name": __file__,
        },
    )
    return RequestLogger(
        logger=logger,
        url_path=req.url.path,
        file_name=__file__,
        log_files=LogFiles(paths_git_status=git_status),
    )
