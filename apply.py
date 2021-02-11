"""
TextbookChecker
this main file include main menu call back function
and connect the other event to editor and etc.

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
import os
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import exceptions
from Element import ui, dialog
from extensions.base import manage

sys.path.append(os.getcwd())  # reset the 'include path' the load the extend
RUN_ONCE = ['coreEditor']  # 立刻加载的插件，一般是ME的基础插件


class TopInterface(object):
    pass  # 解决获取顶层函数问题，部分模块直接使用该接口


class ExtensionsInterface(object):
    pass


class TextFile(object):
    """文本文件类，用于打开，保存文件，以及储存文件状态（替代RUN_STATUS）和更多文件服务"""

    def __init__(self, is_new=True, path='Untitled.txt'):
        """
        初始化文件
        is_new: 是否创建新文件，默认创建新文件
        path: 若读取文件，需要传入path，创建的新文件没有path（None），保存时报错
        """
        self.path = path
        self.isSave = False

        self.bitFile = None
        self.strFile = None
        # create variables end
        if is_new is False:
            self.__load_file()
            UI_WIDGETS.textViewer.insert('1.0', self.strFile)
        else:
            log('Create empty file.')

        UI_WIDGETS.relieveEmptyText()
        MAIN_WINDOW.title(f'{ui.WINDOWS_CONFIG["init_title"]} - {self.path}')

    def __load_file(self):
        """Mark sure file is real,and open it."""
        if (self.path is None) or (not os.path.isfile(self.path)):
            self.path = tkinter.filedialog.askopenfilename(title='Open new file')
            if self.path == '':
                raise exceptions.OpenFileException('User has not choose a file.')  # user choose 'cancel'

        with open(self.path, 'rb') as f:
            self.bitFile = f.read()  # open with bin for encode after load

        try:
            self.strFile = self.bitFile.decode(encoding='utf-8')
        except BaseException as msg:  # I really don't know what is the exception's name
            tkinter.messagebox.showerror('Open error:decode!!!', msg)
            raise exceptions.OpenFileException('Can not decode the file ,please check decode.')

    def save(self, encoding='utf-8'):
        """Save the file with path"""
        content = UI_WIDGETS.textViewer.get('1.0', 'end')[:-1]  # need not the last \n

        if self.path == 'Untitled.txt':
            self.path = tkinter.filedialog.asksaveasfilename(title='Save new file')
            if self.path == '':
                return  # user choose cancel

        with open(self.path, 'wb') as f:
            f.write(content.encode(encoding))
            self.strFile = content  # update memory
        self.isSave = True

    def edit(self, **args):
        """Options here only for receive the event from editor.editEvent ,and not to cause exceptions"""
        self.isSave = False

        log('Edit file from text file.edit')

    def close(self):
        """Make sure file is saved"""
        if self.isSave is False:
            ans = tkinter.messagebox.askyesno('Save', 'File has not saved,save it right now?\n文件未保存，保存？')
            if ans:
                self.save()  # save file

        del self.bitFile, self.strFile, self.path, self.isSave
        UI_WIDGETS.textViewer.delete('1.0', 'end')

        UI_WIDGETS.fillEmptyText()
        MAIN_WINDOW.title(ui.WINDOWS_CONFIG['init_title'])

    def dir(self):
        """Return file's work dir."""
        directory_path = '/'.join(self.path.split('/')[:-1])
        return directory_path


# public member function
def open_file(path=None):
    """Clean up the text and insert new file"""
    try:
        close_file()
    except exceptions.CloseFileException as msg:
        log(msg.__str__())  # 报错多半是首次打开，没文件可以关

    global FILE  # 向file指针上面挂，不然函数返回就没了
    FILE = TextFile(False, path)
    get_element('extension_interfaces>coreEditor>check')(init=True)

    # save file options
    log(f'Opened file {path} successfully')


def close_file():
    """Clean up the window"""
    try:
        FILE.close()
    except AttributeError:  # first run
        raise exceptions.CloseFileException('Have not opened a file.')

    log('Closed file successfully')


def save():
    """Save file with text in text"""
    FILE.save()
    log('save file')


def open_work_dir():
    """Open work directory in Windows Explore"""
    directory_path = FILE.dir()
    os.popen(f'start {directory_path}')
    log('Open work dir successfully')


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


def get_element(arg: str):
    """
    For base extension to get main window's widget,event and function,\n
    pay attention,you must be sure the element's path

    grammar: element's path (father>attribute>attribute...) like UI_WIDGETS>textViewer
    """
    try:
        require_thing_path = arg.split('>')

        attribute = getattr(top, require_thing_path[0])

        for nowAttributeName in require_thing_path[1:]:
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
        get_element(f'extension_interfaces>{name}').onLoad()
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
    FILE = TextFile()  # point to text file in order not to let it deleted

    extension_interfaces = ExtensionsInterface()
    top = _set_top_interface(sys.modules[__name__], dir())

    UI_WIDGETS.openEvent.connect(open_file)
    UI_WIDGETS.openWorkDirEvent.connect(open_work_dir)
    UI_WIDGETS.saveEvent.connect(save)
    UI_WIDGETS.copyContentEvent.connect(copy_content)
    UI_WIDGETS.closeFileEvent.connect(close_file)
    UI_WIDGETS.loadExtensionsEvent.connect(load_extensions)
    # UI connect end

    for extensionRunOnceName in RUN_ONCE:
        load_extensions(extensionRunOnceName)

    MAIN_WINDOW.mainloop()  # 主循环
