import fnmatch
import logging
import os
import subprocess
import uuid
from typing import Any, List, Optional, Tuple

import aiofiles
from pydash import compact, map_

# command = ["git", "status", "-s"]

# result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

# git_status = compact(
#     map_(result.stdout.split("\n"), lambda x: x.split(" ")[1] if x else None)
# )
git_status = []

class CustomFormatter(logging.Formatter):
    green = "\x1b[32;32m"
    blue = "\x1b[34;34m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = """%(levelname)s - %(asctime)s - %(message)s
    - %(name)s - %(url_path)s - %(file_name)s"""

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


current_dir = os.getcwd() + "/"


class LogFiles:
    paths_git_status: List[str] = []
    paths_inserted: List[str] = []

    def __init__(self, paths_git_status: List[str], paths_inserted: List[str]):
        self.paths_git_status = paths_git_status
        self.paths_inserted = paths_inserted

    def paths(self):
        return [*self.paths_git_status, *self.paths_inserted]

    def check_file(self, file_path: str):
        file = file_path.replace(current_dir, "")
        for pattern in self.paths():
            if file == pattern:
                return True
            if fnmatch.fnmatch(file, pattern):
                return True
        return False


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
        if self.__check_files_allowed():
            return self.__direct_log(logging.DEBUG, msg, *args, **kwargs)
        if self.logger.isEnabledFor(logging.DEBUG):
            return self.logger.debug(msg, *args, **kwargs)
        self.buffer.append((logging.DEBUG, msg, args, kwargs))

    def warning(self, msg, *args, **kwargs):
        if self.__check_files_allowed():
            return self.__direct_log(logging.WARNING, msg, *args, **kwargs)
        if self.logger.isEnabledFor(logging.WARNING):
            return self.logger.warning(msg, *args, **kwargs)
        self.buffer.append((logging.WARNING, msg, args, kwargs))

    def info(self, msg, *args, **kwargs):
        if self.__check_files_allowed():
            return self.__direct_log(logging.INFO, msg, *args, **kwargs)
        if self.logger.isEnabledFor(logging.INFO):
            return self.logger.info(msg, *args, **kwargs)
        self.buffer.append((logging.INFO, msg, args, kwargs))

    def error(self, msg, *args, **kwargs):
        if self.__check_files_allowed():
            return self.__direct_log(logging.ERROR, msg, *args, **kwargs)
        if self.logger.isEnabledFor(logging.ERROR):
            return self.logger.error(msg, *args, **kwargs)
        self.buffer.append((logging.ERROR, msg, args, kwargs))

    def exception(self, msg, *args, **kwargs):
        self.__flush()
        self.logger.exception(msg, *args, **kwargs)

    def getChild(self, suffix: str, file: str):
        logger = self.logger.logger.getChild(suffix)
        adapter = self.__make_adapter(logger, file)
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

    def __flush(self):
        if self.parent is not None:
            return self.parent.__flush()
        for lvl, msg, args, kwargs in self.buffer:
            self.__direct_log(lvl, msg, args, **kwargs)
        self.buffer.clear()
        if self.child is not None:
            self.child.parent = None
            self.child.__flush()

    def __direct_log(self, lvl, msg, *args, **kwargs):
        if self.logger.process is not None:
            msg, kwargs = self.logger.process(msg, kwargs)
        self.logger._log(lvl, msg, args, **kwargs)

    def __make_adapter(self, logger: logging.Logger, file: str):
        return logging.LoggerAdapter(
            logger=logger, extra={"url_path": self.url_path, "file_name": file}
        )

    def __check_files_allowed(self):
        return self.log_files.check_file(self.file_name)


def create_logger():
    logger = logging.getLogger("API")
    logger.setLevel(logging.ERROR)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger


async def create_request_logger(
    parent_logger: logging.Logger,
    url_path: str,
):
    request_id = str(uuid.uuid4())
    logger: logging.Logger = parent_logger.getChild(request_id)
    logger = logging.LoggerAdapter(
        logger=logger,
        extra={
            "url_path": url_path,
            "file_name": __file__,
        },
    )
    paths_inserted = []
    # try:
    #     async with aiofiles.open("logs.txt", mode="r") as file:
    #         content = await file.read()
    #         paths_inserted.extend(content.split("\n"))
    # except Exception as e:
    #     logger.warning("file don't exist", exc_info=e)

    return RequestLogger(
        logger=logger,
        url_path=url_path,
        file_name=__file__,
        log_files=LogFiles(paths_git_status=git_status, paths_inserted=paths_inserted),
    )
