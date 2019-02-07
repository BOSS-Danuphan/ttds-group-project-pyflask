import os
import sys
from datetime import datetime
from app import app
from app.utils import sizeof_fmt

class FileWriter:
    _file_path = ""

    def __init__(self, file_path="index.txt"):
        self._file_path = file_path

    def read(self):
        content = None
        try:
            with open(self._file_path, "r") as in_file:
                content = in_file.read()
        except FileNotFoundError:
            print("Read content from {} by {} at {}".format(self._file_path, __name__, datetime.now().strftime(app.config['DATETIME_FORMAT'])))
        else:
            print("Read content from {} by {} at {}".format(self._file_path, __name__, datetime.now().strftime(app.config['DATETIME_FORMAT'])))
        return content

    def write(self, content):
        try:
            with open(self._file_path, "w+") as out_file:
                out_file.write(content)
        except:
            print("Unexpected error at {}.write: {}".format(__name__, sys.exc_info()))
        else:
            print("Content of size {} has been written to {} by {} at {}".format(sizeof_fmt(content), self._file_path, __name__, datetime.now().strftime(app.config['DATETIME_FORMAT'])))
