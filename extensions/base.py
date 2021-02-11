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
    """
    统一的接口，提供给apply，特殊的，这里的baseinterface不需要被继承

    接口有两大工作：1.指向extension让它不要被回收了，2.向外部提供调用接口（绑定事件之类的）
    """
    def __init__(self, extension_obj):
        self._extension = extension_obj
        # point to extension's object ,so that it won't disappear
    def onLoad(self):
        """On load the extension,usually call by apply to let it active"""
        self._extension.onLoad()


# extension 服务类 end
# following are the manage function(just basical function,packed by others)
def _createInterface(extensionObject):
    """
    Create public interface for apply
    :return: public intreface:BaseInterface
    """
    public_interface = BaseInterface(extensionObject)
    attributesList = dir(extensionObject)
    attributesList.remove('onLoad')
    attributesList.remove('unLoad')
    # needn't onload/unload function(usually ,they not call by function except manage)

    for attributeName in attributesList:
        if not attributeName.startswith('_'):
            attribute = getattr(extensionObject, attributeName)
            if callable(attribute):
                setattr(public_interface, attributeName, attribute)

    return public_interface


def manage(kind: str, name: str, **args):
    """
    Import extension's lib and call extension's onLoad member function,will not call onload(need apply)

    :kind: load or unload
        load: name: extensions' name,accessor = get_element
        unload: name: extensions' name,extensions_object = extensions_object

    :return: extension's interface,or None(for unload)
    """
    if kind == 'load':
        packagePath = 'extensions'  # extension lib

        try:
            model_object = importlib.import_module('.'.join((packagePath, name, 'main')))
            extension_object = model_object.Extension(args['accessor'])
            extension_interface = _createInterface(extension_object)
            return extension_interface

        except ImportError as msg:
            print(f'Load extension {name} failed ,please check your extension.')
            return None

    elif kind == 'unload':
        pass  # TODO unload extensions
