"""
TextbookChecker
this main file include main menu call back function
and connect the other event to editor and etc.

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
import tkinter
from coreElement import ui


def openFile():
    log('open file emit')


def openWorkDir():
    log('open work dir')


def save():
    log('save file')


def copyContent():
    log('copy content...')
    content = UI_WIDGETS.contentViewText.get(1.0, 'end')
    import pyperclip
    pyperclip.copy(content)
    del pyperclip


def log(message):
    UI_WIDGETS.statusLabel.config(text=message)


if __name__ == '__main__':
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)

    UI_WIDGETS.openEvent.connect(openFile)
    UI_WIDGETS.openWorkDirEvent.connect(openWorkDir)
    UI_WIDGETS.saveEvent.connect(save)
    UI_WIDGETS.copyContentEvent.connect(copyContent)
    # connect functions end

    MAIN_WINDOW.mainloop()  # 主循环
