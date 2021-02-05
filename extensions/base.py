"""
Base extension for MyEditor
please create extension by using following classes
please override all the member function as possible as you can

copyright: DFSA Software Develop Center
@author: tang142857
"""


class BaseExtension(object):
    """扩展接口"""
    def _getWidgetByName(name: str):
        pass

    def _getEventByName(name: str):
        pass

    def onLoad(MAIN_ARG, **arg):
        pass

    def unLoad():
        pass


class BaseInterface(object):
    """统一的接口，apply可能需要调用 not use widely until 2.0"""
    pass