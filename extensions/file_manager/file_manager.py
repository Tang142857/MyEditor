"""
file serve model for ME

@author: Tang142857
@file: file_manager.py ,Create at: 2021-02-14
Copyright(c): DFSA Software Develop Center
"""
import os
import tkinter.filedialog
import tkinter.messagebox

from Element.main_event import Event
from extensions import base


class TextFile(object):
    """文本文件类，用于打开，保存文件，以及储存文件状态（替代RUN_STATUS）和更多文件服务"""
    def __init__(self, ui, main_window, is_new=True, path='Untitled.txt'):
        """
        初始化文件
        is_new: 是否创建新文件，默认创建新文件
        path: 若读取文件，需要传入path，创建的新文件没有path（None），保存时报错
        """
        self.path = path
        self.isSave = False

        self.bitFile = None
        self.strFile = None
        self.ui = ui
        self.main_window = main_window
        # create variables end
        if is_new is False:
            self.__load_file()
            self.ui.textViewer.insert('1.0', self.strFile)
        else:
            log('Create empty file.')

        self.ui.relieveEmptyText()
        self.main_window.title(f'MyEditor - {self.path}')

    def __load_file(self):
        """Mark sure file is real,and read it into self.bitfile,self.strfile"""
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
        content = self.ui.textViewer.get('1.0', 'end')[:-1]  # need not the last \n

        if self.path == 'Untitled.txt':
            self.path = tkinter.filedialog.asksaveasfilename(title='Save new file')
            if self.path == '':
                return  # user choose cancel

        with open(self.path, 'wb') as f:
            f.write(content.encode(encoding))
            self.strFile = content  # update memory
        self.isSave = True

    def close(self):
        """Make sure file is saved"""
        if self.isSave is False:
            ans = tkinter.messagebox.askyesno('Save', 'File has not saved,save it right now?\n文件未保存，保存？')
            if ans:
                self.save()  # save file

        del self.bitFile, self.strFile, self.path, self.isSave
        self.ui.textViewer.delete('1.0', 'end')

        self.ui.fillEmptyText()
        self.main_window.title('MyEditor')

    def dir(self):
        """Return file's work dir."""
        directory_path = '/'.join(self.path.split('/')[:-1])
        return directory_path


class ManagerMenu(object):
    """此类不一样，附着在file目录下，不需要继承tkinter.menu"""
    def __init__(self, master):
        self._master = master
        self.open_file_event = Event()
        self.write_file_event = Event()
        self.open_directory_event = Event()
        self.close_file_event = Event()
        # create event
        self._master.add_separator()
        self._master.add_command(label='Open File', command=self.open_file_event.emit)
        self._master.add_command(label='Save File', command=self.write_file_event.emit)
        self._master.add_command(label='Close File', command=self.close_file_event.emit)
        self._master.add_command(label='Open Directory', command=self.open_directory_event.emit)
        # create menu labels


class Manager(base.BaseExtension):
    """File manage serve for me editor"""
    def __init__(self, accessor):
        super(Manager, self).__init__(accessor)

    def on_load(self, **arg):
        global log
        log = self._get_element('log')

        self._menu = ManagerMenu(self._get_element('UI_WIDGETS>fileMenu'))
        self._file = TextFile(self._get_element('UI_WIDGETS'), self._get_element('MAIN_WINDOW'))

        self._menu.open_directory_event.add_callback(self.go_directory)
        self._menu.open_file_event.add_callback(self.open_file)
        self._menu.write_file_event.add_callback(self.save_file)
        self._menu.close_file_event.add_callback(self.close_file)

    def un_load(self):
        pass

    def open_file(self, event):
        """关闭上一文件，询问文件位置，初始化新文件，调用全文检查"""
        self.close_file(None)

        try:
            file_path = event.path
        except AttributeError:
            file_path = tkinter.filedialog.askopenfilename()
            if not bool(file_path): return

        self._file = TextFile(self._get_element('UI_WIDGETS'),
                              self._get_element('MAIN_WINDOW'),
                              is_new=False,
                              path=file_path)

        self._get_element('extension_interfaces>core_editor>check')(init=True)

    def save_file(self, event):
        self._file.save()
        log('Saved file.')

    def close_file(self, event):
        """关闭文件，锁定viewer"""
        try:
            self._file.close()
        except BaseException as msg:
            print(msg)

        self._get_element('UI_WIDGETS').fillEmptyText()
        log('Close file.')

    def go_directory(self, event):
        directory_path = self._file.dir()
        os.popen(f'start {directory_path}')
        log(f'Go directory {directory_path}')
