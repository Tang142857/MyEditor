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
            self._load_file()
        else:
            log('Create empty file.')

        self.push()
        self.ui.relieveEmptyText()

    def _load_file(self):
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

        if not os.path.isdir('/'.join(path.split('/')[:-1])):
            path = tkinter.filedialog.asksaveasfilename()
            if not bool(path): return  # the user press cancel

        with open(path, 'wb') as f:
            # update bit file ,file path ,write file
            self.bit_file = self.str_file.encode(encoding)
            self.path = path
            f.write(self.bit_file)

    def close(self):
        """release objects ,fill window ,and clean viewer"""
        self.ui.textViewer.delete('1.0', 'end')
        self.ui.fillEmptyText()
        del self.bit_file, self.str_file, self.path, self.ui

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
        self.write_new_file_event = main_event.Event()
        self.open_directory_event = main_event.Event()
        self.close_file_event = main_event.Event()
        # create event
        self._master.add_separator()
        self._master.add_command(label='Open File', command=self.open_file_event.emit)
        self._master.add_command(label='Save File', command=self.write_file_event.emit)
        self._master.add_command(label='Save File As', command=self.write_new_file_event.emit)
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
        self._file = TextFile(self._get_element('UI_WIDGETS'))

        self._menu.open_directory_event.add_callback(self.go_directory)
        self._menu.open_file_event.add_callback(self.open_file)
        self._menu.write_file_event.add_callback(self.save_file)
        self._menu.close_file_event.add_callback(self.close_file)
        self._menu.write_new_file_event.add_callback(self.save_file_as)

    def un_load(self):
        pass

    # ######## extension's requirement function definition end #######
    # public function definition begin here.

    def open_file(self, event=None):
        """close the next file ,make sure the path ,call editor"""
        self.close_file()
        path = tkinter.filedialog.askopenfilename()
        if not bool(path): return  # user press cancel
        self._file = TextFile(self._get_element('UI_WIDGETS'), False, path)

        self._get_element('extension_interfaces>core_editor>check')(init=True)

    def save_file(self, event=None):
        """save the file at its origin position ,if new ,file object will ask path"""
        if self._file is not None:
            self._file.pull()
            self._file.write()

    def save_file_as(self, event=None):
        """Ask new path and save"""
        if self._file is not None:
            new_path = tkinter.filedialog.asksaveasfilename()
            if not bool(new_path): return  # user press cancel
            self._file.pull()
            self._file.write(new_path)

    def close_file(self, event=None):
        """close now file"""
        if self._file is not None:
            if not self._file.compare():
                user_answer = tkinter.messagebox.askyesno('Save?', 'File had not been saved ,save it right now?')
                if user_answer: self.save_file()
            self._file.close()
            self._file = None

    def go_directory(self, event=None):
        directory_path = self._file.dir()
        os.popen(f'start {directory_path}')
        log(f'Go directory {directory_path}')
