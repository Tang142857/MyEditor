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


class ArgumentPackage(object):
    pass


class Event(object):
    """
    Stronger event object ,it allow you to add args,and pass to callbacks with event...
    Now ,you can pass arguments even emit the event.
    But pay attention all arguments will be packed in event_args.
    """
    def __init__(self, **args):
        self.callback_functions = []
        self.event_args = ArgumentPackage()
        for arg in args:  # bind arguments
            setattr(self.event_args, arg, args[arg])

    def add_callback(self, func):
        assert callable(func), 'ERROR_IS_NOT_CALLABLE'
        self.callback_functions.append(func)

    def emit(self, *arg, **args):
        # TODO async rewrite
        for argument in arg:
            setattr(self.event_args, 'emit_arg', argument)
        for argument in args:
            setattr(self.event_args, argument, args[argument])
        self._call()

    def _call(self):
        for cell in self.callback_functions:
            cell(self.event_args)


class BaseEvent(object):
    """Base event"""
    def __init__(self):
        self.callList = []

    def connect(self, func):
        if callable(func):
            self.callList.append(func)
        else:
            raise ConnectException(str(func) + ' can not be called.')

    def add_callback(self, func):
        self.connect(func)

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


class BaseEventWithArgument(BaseEvent):
    """Base event"""
    def __init__(self):
        self.callList = []
        self.arguments = {}

    def addArgument(self, name, value):
        """Add new argument to argument dictionary."""
        self.arguments[name] = value

    def connect(self, func):
        """Connect the function to event."""
        if callable(func):
            self.callList.append(func)
        else:
            raise ConnectException(str(func) + ' can not be called.')

    def _do(self):
        """Call all the connected function."""
        for func in self.callList:
            func(**self.arguments)  # work through the call list and call functions

    def decider(self):
        """Decide whether do the action or not,you may override the function"""
        self._do()

    def emit(self, event=None):
        """Emit the event."""
        self.addArgument('event', event)
        self.decider()


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


class CloseFileEvent(BaseEvent):
    def __init__(self):
        super().__init__()


class LoadExtensionsEvent(BaseEvent):
    def __init__(self):
        super().__init__()


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
