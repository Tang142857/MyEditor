"""
file serve model for ME

@author: Tang142857
@project: MyEditor
@file: file_manager.py
@date: 2021-02-22
Copyright(c): DFSA Software Develop Center
"""
import os
from hashlib import md5
import tkinter.filedialog
import tkinter.messagebox

import exceptions
from Element import main_event, dialog, share_memory
from extensions import base


class TextFile(object):
    """文本文件类，用于打开，保存文件，以及储存文件状态（替代RUN_STATUS）和更多文件服务"""
    def __init__(self, ui, is_new=True, path='Untitled.txt'):
        """
        初始化文件
        is_new: 是否创建新文件，默认创建新文件
        path: 若读取文件，需要传入path，创建的新文件没有path（None），保存时报错

        First save the path ,even it is untitled ,untitled file path is none.
        Second ,create bit file ,str file ,save ui's pointer.
        """
        self.path = path

        self.bit_file = 0x0000
        self.str_file = str()
        self.ui = ui
        # create variables end
        if is_new is False:
            self.__load_file()
        else:
            log('Create empty file.')

        self.push()
        self.ui.relieveEmptyText()

    def __load_file(self):
        with open(self.path, 'rb') as f:
            self.bit_file = f.read()  # open with bin for encode after load

        try:
            self.str_file = self.bit_file.decode(encoding='utf-8')
        except UnicodeDecodeError as msg:
            tkinter.messagebox.showwarning('Encoding',
                                           'File is opened ,but encoding is not utf-8 ,please check and reload.')
            self.str_file = str(self.bit_file)

    def write(self, path=None, encoding='utf-8'):
        """Write self.str_file to disk"""
        if path is not None:
            pass
        else:
            path = self.path

        if not os.path.isfile(path):
            path = tkinter.filedialog.askopenfilename()
            if not bool(path): return  # the user press cancel

        with open(path, 'wb') as f:
            self.bit_file = self.str_file.encode(encoding)
            f.write(self.bit_file)

    def close(self):
        """release objects ,fill window ,and clean viewer"""
        del self.bit_file, self.str_file, self.path, self.ui
        self.ui.textViewer.delete('1.0', 'end')
        self.ui.fillEmptyText()

    def dir(self):
        """Return file's work dir."""
        directory_path = '/'.join(self.path.split('/')[:-1])
        return directory_path

    def push(self):
        """Push now str file to viewer"""
        self.ui.textViewer.delete('1.0', 'end')
        self.ui.textViewer.insert('insert', self.str_file)

    def pull(self):
        """Pull viewer's file to self.str_file"""
        content = self.ui.textViewer.get('1.0', 'end')[:-1]  # need not the last \n
        self.str_file = content

    def compare(self):
        """Compare viewer's file and self.str_file"""
        self_md5 = md5(self.str_file.encode('utf-8')).hexdigest()
        viewer_md5 = md5((self.ui.textViewer.get('1.0', 'end')[:-1]).encode('utf-8')).hexdigest()
        return viewer_md5 == self_md5


class ManagerMenu(object):
    """此类不一样，附着在file目录下，不需要继承tkinter.menu"""
    def __init__(self, master):
        self._master = master
        self.open_file_event = main_event.Event()
        self.write_file_event = main_event.Event()
        self.open_directory_event = main_event.Event()
        self.close_file_event = main_event.Event()
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
        """关闭文件"""
        try:
            self._file.close()
        except AttributeError as msg:
            pass  # 多半是在没有打开文件的情况下open，没有上一个文件可关闭
        finally:
            self._file = None
            self._get_element('UI_WIDGETS').fillEmptyText()
            log('Close file.')

    def go_directory(self, event):
        directory_path = self._file.dir()
        os.popen(f'start {directory_path}')
        log(f'Go directory {directory_path}')
