"""
TextbookChecker
this main file include main menu call back function
and connect the other event to editor and etc.

@author: Tang142857
@file: apply.py ,Create at: 2021-02-14
Copyright(c): DFSA Software Develop Center
"""
import os
import sys
import tkinter
import tkinter.messagebox

import exceptions
from Element import ui, dialog
from extensions.base import manage

sys.path.append(os.getcwd())  # reset the 'include path' the load the extend
RUN_ONCE = ['file_manager', 'core_editor']  # 立刻加载的插件，一般是ME的基础插件


class TopInterface(object):
    """Top interface of main window,for get_element to call"""
    pass  # 解决获取顶层函数问题，部分模块直接使用该接口


class ExtensionsInterface(object):
    """Extensions' public interface, use 'extension_interfaces.extension_name.func' to call"""
    pass  # 各个插件的公共接口


def copy_content():
    content = UI_WIDGETS.textViewer.get('0.0', 'end')
    import pyperclip
    pyperclip.copy(content)
    del pyperclip

    log('Copy content successfully.')


def log(message):
    UI_WIDGETS.statusLabel.config(text=message)


def console_log(message, **args):
    string = f'{__file__}:{message}'
    print(string)


def get_element(element_path: str):
    """
    For base extension to get main window's widget,event and function,\n
    pay attention,you must be sure the element's path

    grammar: element's path (father>attribute>attribute...) like UI_WIDGETS>textViewer
    """
    try:
        listed_element_path = element_path.split('>')

        attribute = getattr(top, listed_element_path[0])

        for nowAttributeName in listed_element_path[1:]:
            attribute = getattr(attribute, nowAttributeName)

        return attribute

    except Exception as msg:
        print(msg)
        return None


def load_extensions(name=''):
    """A function bases on extensions.base.manage to load extensions. Call by: self,ui"""
    if name == '':
        name = dialog.ask_extension_name()
        if name is None:
            return
    else:
        pass

    extension_interface = manage('load', name, accessor=get_element)
    if extension_interface is not None:
        setattr(extension_interfaces, name, extension_interface)
        log(f'Activating the extension {name}...')
        get_element(f'extension_interfaces>{name}').on_load()
    else:
        log(f'Load {name} extension failed.')


# protected member function,do not call this function
def _set_top_interface(me, model_attribute_names):
    """Create top interface for other extensions"""
    top_interface = TopInterface()

    for modelAttributeName in model_attribute_names:
        if not modelAttributeName.startswith('_'):
            attribute_obj = getattr(me, modelAttributeName)
            setattr(top_interface, modelAttributeName, attribute_obj)

    return top_interface


if __name__ == '__main__':
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)
    UI_WIDGETS.fillEmptyText()

    extension_interfaces = ExtensionsInterface()
    top = _set_top_interface(sys.modules[__name__], dir())

    UI_WIDGETS.copyContentEvent.connect(copy_content)
    UI_WIDGETS.loadExtensionsEvent.connect(load_extensions)
    # UI connect end

    for extensionRunOnceName in RUN_ONCE:
        load_extensions(extensionRunOnceName)

    MAIN_WINDOW.mainloop()  # 主循环
