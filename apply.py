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

from coreEditor import editor
from coreElement import ui
from coreElement.mainEvent import EditEvent

sys.path.append(os.getcwd())  # reset the 'include path' the load the extend

RUN_STATUS = {'isOpened': False, 'isSaved': False, 'openedFilePath': ''}


class CloseFileException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message


def openFile(path=None):
    """Clean up the text and insert new file"""
    try:
        closeFile()  # close the last file
    except CloseFileException:
        pass
    finally:
        UI_WIDGETS.relieveEmptyText()  # relieve the content viewer

    if (path is None) or (not os.path.isfile(path)):
        path = tkinter.filedialog.askopenfilename(title='Open')
        if path == '':
            return  # 用户点击取消

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    UI_WIDGETS.contentViewText.insert('1.0', content)
    # read file and write them into text

    RUN_STATUS['isOpened'] = True
    RUN_STATUS['openedFilePath'] = path
    # save file options
    log(f'Opened file {path} successfully')


def closeFile():
    """Clean up the window"""
    if RUN_STATUS['isOpened'] is False:
        raise CloseFileException('Have not opened a file.')
    else:
        UI_WIDGETS.contentViewText.delete('1.0', 'end')
        UI_WIDGETS.fillEmptyText()

        RUN_STATUS['isOpened'] = False
        RUN_STATUS['openedFilePath'] = ''
        # Change status to closed
        log('Closed file successfully')


def openWorkDir():
    log('open work dir')


def save():
    log('save file')


def copyContent():
    content = UI_WIDGETS.contentViewText.get('0.0', 'end')
    import pyperclip
    pyperclip.copy(content)
    del pyperclip

    log('Copy content successfully.')


def log(message):
    UI_WIDGETS.statusLabel.config(text=message)


if __name__ == '__main__':
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)
    editor.setTags(UI_WIDGETS.contentViewText)  # config tags for color

    # Some event emitted by MAIN_WINDOW should create for extend(include editor)
    editEvent = EditEvent(UI_WIDGETS.contentViewText)

    UI_WIDGETS.openEvent.connect(openFile)
    UI_WIDGETS.openWorkDirEvent.connect(openWorkDir)
    UI_WIDGETS.saveEvent.connect(save)
    UI_WIDGETS.copyContentEvent.connect(copyContent)
    UI_WIDGETS.closeFileEvent.connect(closeFile)
    # UI connect end
    editEvent.connect(editor.check)
    # extend connect with MAIN_WINDOW
    editor.logEvent.connect(log)
    # connect functions end

    MAIN_WINDOW.bind('<KeyRelease>', editEvent.emit)
    UI_WIDGETS.fillEmptyText('Welcome')

    MAIN_WINDOW.mainloop()  # 主循环
