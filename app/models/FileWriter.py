import os

class FileWriter:
    _file_path = ""

    def __init__(self, file_path="index.txt"):
        self._file_path = file_path

    def read(self):
        try:
            with open(self._file_path, "r") as in_file:
                return in_file.read()
        except FileNotFoundError:
            return None

    def write(self, content):
        with open(self._file_path, "w+") as out_file:
            out_file.write(content)