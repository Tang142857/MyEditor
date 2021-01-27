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
from coreEditor import editor
from Element import ui
from Element.mainEvent import EditEvent

sys.path.append(os.getcwd())  # reset the 'include path' the load the extend


class TextFile(object):
    """文本文件类，用于打开，保存文件，以及储存文件状态（替代RUN_STATUS）和更多文件服务"""
    def __init__(self, isNew=True, path='Untitle.txt'):
        """
        初始化文件
        isNew: 是否创建新文件，默认创建新文件
        path: 若读取文件，需要传入path，创建的新文件没有path（None），保存时报错
        """
        self.path = path
        self.isSave = False

        self.bitFile = None
        self.strFile = None
        # create variables end
        if isNew is False:
            self.__loadFile()
            UI_WIDGETS.textViewer.insert('1.0', self.strFile)
        else:
            log('Create empty file.')

        UI_WIDGETS.relieveEmptyText()
        MAIN_WINDOW.title(f'{ui.WINDOWS_CONFIG["init_title"]} - {self.path}')

    def __loadFile(self):
        """Mark sure file is real,and open it."""
        if (self.path is None) or (not os.path.isfile(self.path)):
            self.path = tkinter.filedialog.askopenfilename(title='Open new file')
            if self.path == '':
                raise exceptions.OpenFileException('User has not choose a file.')  # user choose 'cancl'

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

        if self.path == 'Untitle.txt':
            self.path = tkinter.filedialog.asksaveasfilename(title='Save new file')
            if self.path == '': return  # user choose cancal

        with open(self.path, 'wb') as f:
            f.write(content.encode(encoding))
            self.strFile = content  # update memory
        self.isSave = True

    def edit(self, **args):
        """Options here only for receive the event from editor.editEvent ,and not to cause exceptions"""
        self.isSave = False

        log('Edit file from textfile.edit')

    def close(self):
        """Make sure file is saved"""
        if self.isSave is False:
            ans = tkinter.messagebox.askyesno('Save', 'File has not saved,save it right now?\n文件未保存，保存？')
            if ans: self.save()  # save file

        del self.bitFile, self.strFile, self.path, self.isSave, self.isOpened
        UI_WIDGETS.textViewer.delete('1.0', 'end')

        UI_WIDGETS.fillEmptyText()
        MAIN_WINDOW.title(ui.WINDOWS_CONFIG['init_title'])

    def dir(self):
        """Return file's work dir."""
        directoryPath = '/'.join(self.path.split('/')[:-1])
        return directoryPath


def openFile(path=None):
    """Clean up the text and insert new file"""
    try:
        closeFile()
    except exceptions.CloseFileException as msg:
        log(msg.__str__())  # 报错多半是首次打开，没文件可以关

    global FILE  # 向file指针上面挂，不然函数返回就没了
    FILE = TextFile(False, path)

    # save file options
    editEvent.emit('Call by apply.openFile')
    log(f'Opened file {path} successfully')


def closeFile():
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


def openWorkDir():
    """Open work directory in Windows Explore"""
    directoryPath = FILE.dir()
    os.popen(f'start {directoryPath}')
    log('Open work dir successsfully')


def copyContent():
    content = UI_WIDGETS.textViewer.get('0.0', 'end')
    import pyperclip
    pyperclip.copy(content)
    del pyperclip

    log('Copy content successfully.')


def log(message):
    UI_WIDGETS.statusLabel.config(text=message)


if __name__ == '__main__':
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)
    UI_WIDGETS.fillEmptyText()
    FILE = TextFile()  # point to text file in order not to let it deleted

    extendInitArgs = {
        'MAIN_WINDOW': MAIN_WINDOW,
        'UI_WIDGETS': UI_WIDGETS,
        'MAIN_CALL': {
            'log': log,
            'copy_content': copyContent,
            'open_file': openFile,
            'open_work_dir': openWorkDir,
            'save': save,
            'close_file': closeFile
        }
    }
    # initialize extend
    editor.initialize(**extendInitArgs)

    # Some event emitted by MAIN_WINDOW should create for extend(include editor)
    editEvent = EditEvent()

    UI_WIDGETS.openEvent.connect(openFile)
    UI_WIDGETS.openWorkDirEvent.connect(openWorkDir)
    UI_WIDGETS.saveEvent.connect(save)
    UI_WIDGETS.copyContentEvent.connect(copyContent)
    UI_WIDGETS.closeFileEvent.connect(closeFile)
    # UI connect end
    editEvent.connect(FILE.edit)
    editEvent.connect(editor.check)
    # extend connect with MAIN_WINDOW

    MAIN_WINDOW.bind('<KeyRelease>', editEvent.emit)

    MAIN_WINDOW.mainloop()  # 主循环
