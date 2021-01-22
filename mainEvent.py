"""
Model that include all event.
@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""


class ConnectException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class BaseEvent(object):
    """Base event"""
    def __init__(self):
        self.callList = []

    def connect(self, func):
        if callable(func):
            self.callList.append(func)
        else:
            raise ConnectException(str(func) + ' can not be called.')

    def emit(self):
        for func in self.callList:
            func()  # work through the call list and call functions


def test_fun():
    print('call!')


if __name__ == "__main__":
    event = BaseEvent()
    event.connect(test_fun)
    event.connect(test_fun)
    event.emit()
