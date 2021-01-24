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

    def _do(self):
        """Call all the connected function."""
        for func in self.callList:
            func()  # work through the call list and call functions

    def decider(self, event=None):
        """Decide whether do the action or not,you may override the function"""
        self._do()

    def emit(self, event=None):
        """Emit the event."""
        self.decider(event)


class OpenEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class SaveEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class OpenWorkDirEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class CopyContentEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class EditEvent(BaseEvent):
    def __init__(self, text):
        super().__init__()
        self.text = text  # send to editor.check

    def _do(self, event):
        """Override do to send text for editor.check"""
        for func in self.callList:
            func(self.text, event)

    def decider(self, event=None):
        self._do(event)


class CloseFileEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class EditorLogEvent(BaseEvent):
    """Override the BE to send log to status label"""
    def __init__(self):
        super().__init__()

    def _do(self, message):
        for func in self.callList:
            func(message)

    def decider(self, message):
        self._do(message)


class ExampleEvent(BaseEvent):
    """Example class to test."""
    def __init__(self):
        super().__init__()
        self.lock = True

    def decider(self, event=None):
        if self.lock:
            self._do()
        else:
            return

    def lockMe(self):
        self.lock = False


def test_fun():
    print('call!')


if __name__ == "__main__":
    event = ExampleEvent()
    event.connect(test_fun)
    event.connect(test_fun)
    event.emit()
    event.lockMe()
    event.emit()
