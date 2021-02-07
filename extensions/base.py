"""
Base extension for MyEditor
please create extension by using following classes
please override all the member function as possible as you can

copyright: DFSA Software Develop Center
@author: tang142857
"""
import importlib  # for load extension function


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


def loadExtensions(name: str, getElement):
    """
    Import extension's lib and call extension's onLoad member function
    :return: extension's interface object
    """
    packagePath = 'extensions'  # extension lib
    try:
        model = importlib.import_module('.'.join((packagePath, name, 'main')))
        interface = model.Extension(getElement)
        interface.onLoad()
        return interface
    except ImportError as msg:
        print(f'Load extension {name} failed ,please check your extension.')
