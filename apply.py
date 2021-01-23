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

from coreEditor import editor
from coreElement import ui
from coreElement.mainEvent import EditEvent

sys.path.append(os.getcwd())  # reset the 'include path' the load the extend


def openFile():
    log('open file emit')


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
