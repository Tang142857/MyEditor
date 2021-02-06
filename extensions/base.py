"""
Base extension for MyEditor
please create extension by using following classes
please override all the member function as possible as you can

copyright: DFSA Software Develop Center
@author: tang142857
"""


class BaseExtension(object):
    """
    扩展接口
    Please override every member function that are not protected.
    Please use super.func() for every protected member function.
    """
    def __init__(self, interface):
        self.getElementFromMain = interface

    def _getElement(self, EPath):
        return self.getElementFromMain(EPath)

    def onLoad(self, **arg):
        pass

    def unLoad():
        pass


class BaseInterface(object):
    """统一的接口，apply可能需要调用 not use widely until 2.0"""
    pass


def loadExtensions(name: str):
    pass  # TODO load extensions
