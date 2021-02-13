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
    Please use the same init function ,like core_editor
    Please add function you need into child class,it well add into public 
    interface(surely except protected function)

    need override:on_load,un_load(core extension use pass)
    """
    def __init__(self, interface):
        self.accessor = interface

    def _get_element(self, path):
        return self.accessor(path)

    def on_load(self, **arg):
        pass

    def un_load(self):
        pass


class BaseInterface(object):
    """
    统一的接口，提供给apply，特殊的，这里的base interface不需要被继承

    接口有两大工作：1.指向extension让它不要被回收了，2.向外部提供调用接口（绑定事件之类的）
    """
    def __init__(self, extension_obj):
        self._extension = extension_obj
        # point to extension's object ,so that it won't disappear

    def on_load(self):
        """On load the extension,usually call by apply to let it active"""
        self._extension.on_load()


# extension 服务类 end
# following are the manage function(just basical function,packed by others)
def _create_interface(extension_object):
    """
    Create public interface for apply
    :return: public intreface:BaseInterface
    """
    public_interface = BaseInterface(extension_object)
    attributesList = dir(extension_object)
    attributesList.remove('on_load')
    attributesList.remove('un_load')
    # needn't load/unload function(usually ,they not call by function except manage)

    for attributeName in attributesList:
        if not attributeName.startswith('_'):
            attribute = getattr(extension_object, attributeName)
            if callable(attribute):
                setattr(public_interface, attributeName, attribute)

    return public_interface


def manage(kind: str, name: str, **args):
    """
    Import extension's lib and call extension's on_load member function,will not call onload(need apply)

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
            extension_interface = _create_interface(extension_object)
            return extension_interface

        except ImportError as msg:
            print(f'Load extension {name} failed ,please check your extension.')
            print(msg)
            return None

    elif kind == 'unload':
        pass  # TODO unload extensions
