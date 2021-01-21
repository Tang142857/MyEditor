"""
TextbookChecker
@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""

import json
import os
import re
import tkinter
import tkinter.messagebox
from time import localtime, strftime, time

from tool import book
from tool import debug
from tool import ui


class BookEditor(object):
    """
    The editor of the book object.
    Using load book to load new book.When the program start running ,it will call the funcion ,too.
    Using set next/last page to set pages.The counter will get the right page :)
    """
    def __init__(self):
        self.data = None
        self.nowChapterNumber = 0
        self.nowChapter = []
        self.workEnvironment = {}
        # Initialize the attributes

    def __getPath(self, Paths: str):
        """Get the file's directory."""
        baseFileName = re.split(r'[\\/]', Paths)[-1]  # To get the file name.
        # Replace the origin file with empty char is ok.
        return Paths.replace(baseFileName, '')

    def getWorkDirectory(self):
        """Accessor of workEnvironment.workDirectory"""
        return self.workEnvironment['workDirectoryPath']

    def loadBook(self, path: str):
        self.workEnvironment['workFilePath'] = path
        self.workEnvironment['workDirectoryPath'] = self.__getPath(path)
        self.data = book.decodeBook(path)
        # Load book end

        MAIN_WINDOW.title('Text Book Reader-' + path)  # Reset the title of the main window.

    def setNextPage(self, viewer):
        self.nowChapterNumber += 1
        self.update(viewer=viewer)
        log(f'Next page ,number {self.nowChapterNumber}')

    def setLastPage(self, viewer):
        self.nowChapterNumber -= 1
        self.update(viewer=viewer)
        log(f'Review page ,number {self.nowChapterNumber}')

    def update(self, viewer):
        """Update the text with now page number."""
        viewer.delete(1.0, 'end')  # Clean up the viewer.
        viewer.insert('end', self.data.getChapter(self.nowChapterNumber))


class EventHost(object):

    def updateViewer(self):
        EDITOR.update(UI_WIDGETS.contentViewText)

    def nextPageEvent(self, event=None):
        # Page change event receive the TK's and ui's signal.
        EDITOR.setNextPage(UI_WIDGETS.contentViewText)

    def reviewPageEvent(self, event=None):
        # Page change event receive the TK's and ui's signal.
        EDITOR.setLastPage(UI_WIDGETS.contentViewText)

    def setBookPath(self):
        """
        Set an new book.
        """
        def setNewBookPath():
            newPath = setWidgets.inputWidget.get()
            if os.path.isfile(newPath):
                printStatus(f'new path {newPath}')
                EDITOR.loadBook(newPath)
            else:
                tkinter.messagebox.showwarning('Warning', 'File can not be read,please check your path.')
            setBookPathWindow.quit()
            setBookPathWindow.destroy()  # toplevel的玄学东西，quit之后还要加上destroy

        setBookPathWindow = tkinter.Toplevel()
        setWidgets = ui.SetBookPathWindow(setBookPathWindow, setNewBookPath)
        setBookPathWindow.mainloop()

    def copyContent(self):
        """
        Copy now content to copyboard
        """
        import pyperclip
        nowContent = UI_WIDGETS.contentViewText.get(1.0, 'end')
        pyperclip.copy(nowContent)
        log('Copy context to clip...')
        del pyperclip  # Clean up the memory

    def saveFile(self):
        """Save file to the formatted file."""
        printStatus('Saving file.')  # TODO save file

    def openWorkDirectory(self):
        nowWorkDirectory = EDITOR.getWorkDirectory()
        if ' ' in nowWorkDirectory:
            log('Open exception.')
            tkinter.messagebox.showwarning('Path exception', 'Can not open directory with empty char like \\s')
        else:  # if there some empty chars in path ,can not open the directory with windows explorer
            log(f'Going to {nowWorkDirectory}')
            os.popen(f'start {nowWorkDirectory}')


def printStatus(values, end='\n', head=''):
    """
    Print the value with time string and status string.
    :param head: sting head just like \r
    :param end: string end just like \n
    :param values: value
    :return: nothing
    """
    originTime = localtime(time())  # 创建本地时间
    time_string = strftime('%H:%M:%S', originTime)  # 生成时间戳
    print(f'{head}INFO:{time_string} :: {values}', end=end)


def windowConfig(event):
    # print(event)
    log(event.__str__())


def log(string: str):
    """Print the status on status label"""
    UI_WIDGETS.statusLabel.config(text=string)


if __name__ == "__main__":
    with open('resource/configure.json', 'r', encoding='utf-8') as configure:
        CONFIGURE = json.loads(configure.read())
    print(CONFIGURE)
    # Load configure file end.

    MAIN_WINDOW = tkinter.Tk()
    EDITOR = BookEditor()
    EVENT_HOST = EventHost()
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW, EVENT_HOST)  # 加载主窗体UI
    # Creating objects end.
    # EVENT_HOST.setEditor(EDITOR)
    # initialize object end

    EDITOR.loadBook(CONFIGURE['bookPath'])  # Preload the default book.
    EVENT_HOST.updateViewer()  # Update the viewer to display the first page.

    MAIN_WINDOW.bind('<Configure>', windowConfig)  # Listening to window config event and log on status label
    MAIN_WINDOW.bind('<Left>', EVENT_HOST.reviewPageEvent)
    MAIN_WINDOW.bind('<Right>', EVENT_HOST.nextPageEvent)

    MAIN_WINDOW.mainloop()  # Calling main loop.
