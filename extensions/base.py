"""
Base extension for MyEditor
please create extension by using following classes
please override all the member function as possible as you can

copyright: DFSA Software Develop Center
@author: tang142857
"""


class BaseExtension(object):
    """扩展接口"""
    def _getElement(EPath):
        return self.getElementFromMain(EPath)

    def onLoad(getElement, **arg):
        self.getElementFromMain = getElement

    def unLoad():
        pass


class BaseInterface(object):
    """统一的接口，apply可能需要调用 not use widely until 2.0"""
    pass


def loadExtensions(name: str):
    pass  # TODO load extensions
