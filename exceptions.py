"""
TextbookChecker
this exceptions file include all exception in apply.py

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""


class CloseFileException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class OpenFileException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class SaveFileException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message