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


def manage(kind: str, name: str, **args):
    """
    Import extension's lib and call extension's onLoad member function
    :kind: load or unload
    load: name: extensions' name,accessor = getElement
    unload: name: extensions' name,extensions_object = extensions_object
    :return: extension's interface object,or None(for unload)
    """
    if kind == 'load':
        packagePath = 'extensions'  # extension lib

        try:
            model = importlib.import_module('.'.join((packagePath, name, 'main')))
            model_object = model.Extension(args['accessor'])
            model_object.onLoad()
            return model_object

        except ImportError as msg:
            print(f'Load extension {name} failed ,please check your extension.')
            return None

    elif kind == 'unload':
        pass  # TODO unload extensions
