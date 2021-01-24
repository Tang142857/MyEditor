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

RUN_STATUS = {'isOpened': False, 'isSaved': False}


def openFile(path=None):
    log('open file emit')
    if (path is None) or (not os.path.isfile(path)):
        path = tkinter.filedialog.askopenfilename(title='Open')
    # ask path end
    log(f'Opening file {path}')

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # read file and write them into text
    UI_WIDGETS.contentViewText.insert('1.0', content)


def openWorkDir():
    log('open work dir')


def save():
    log('save file')


def copyContent():
    log('copy content...')
    content = UI_WIDGETS.contentViewText.get('0.0', 'end')
    import pyperclip
    pyperclip.copy(content)
    del pyperclip


def log(message):
    UI_WIDGETS.statusLabel.config(text=message)


if __name__ == '__main__':
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)
    editor.setTags(UI_WIDGETS.contentViewText)  # config tags for color
    UI_WIDGETS.contentViewText.insert('insert', 'Hello World', 'say')
    UI_WIDGETS.contentViewText.delete('1.1', '1.1')

    # Some event emitted by MAIN_WINDOW should create for extend(include editor)
    editEvent = EditEvent(UI_WIDGETS.contentViewText)

    UI_WIDGETS.openEvent.connect(openFile)
    UI_WIDGETS.openWorkDirEvent.connect(openWorkDir)
    UI_WIDGETS.saveEvent.connect(save)
    UI_WIDGETS.copyContentEvent.connect(copyContent)
    # UI connect end
    editEvent.connect(editor.check)
    # extend connect with MAIN_WINDOW
    editor.logEvent.connect(log)
    # connect functions end

    MAIN_WINDOW.bind('<KeyRelease>', editEvent.emit)

    MAIN_WINDOW.mainloop()  # 主循环
