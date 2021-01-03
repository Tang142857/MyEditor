"""
TextbookChecker
@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
import json
import tkinter
import re
import tkinter.messagebox
import os
from time import localtime, strftime, time
import ui
import debug


class Book(object):
    def __init__(self):
        self.data = {'info': {}, 'body': []}
        # Initialize book object finish.

    def __str__(self):
        """Override the str function to pretty print."""
        string = self.data['info']
        return 'INFO:' + str(string)

    def addInfo(self, infoName, newInformation):
        self.data['info'][infoName] = newInformation

    def addChapter(self, chapter: str):
        self.data['body'].append(chapter)

    def getChapter(self, chapterIndex: int):
        return self.data['body'][chapterIndex]

    def getInfo(self, informationName):
        return self.data['info'][informationName]


class BookEditor(object):
    """
    The editor of the book object.
    Using load book to load new book.When the program start running ,it will call the funcion ,too.
    Using set next/last page to set pages.The counter will get the right page :)
    """
    def getPath(self, Paths: str):
        """Make the formated book name."""
        baseFileName = re.split(r'[\\/]', Paths)[-1]  # To get the file name.
        # fileExtendName = '.' + re.split(r'\.', baseFileName)[-1]  # To get the extend name.
        # newFileName = '$' + baseFileName.replace(fileExtendName, '$' + fileExtendName)
        return Paths.replace(baseFileName, '')

    def getWorkDirectory(self):
        return self.workDirectory

    def loadBook(self, path: str):
        self.originalBookPath = path
        self.workDirectory = self.getPath(path)
        self.pageNumber = 0
        self.data = normalDecoder(path=path)
        # Load book end

        MAIN_WINDOW.title('Text Book Reader-' + path)  # Reset the title of the main window.

    def setNextPage(self, viewer):
        self.pageNumber += 1
        self.update(viewer=viewer)
        log(f'Next page ,number {self.pageNumber}')

    def setLastPage(self, viewer):
        self.pageNumber -= 1
        self.update(viewer=viewer)
        log(f'Review page ,number {self.pageNumber}')

    def update(self, viewer):
        """Update the text with now page number."""
        viewer.delete(1.0, 'end')  # Clean up the viewer.
        viewer.insert('end', self.data.getChapter(self.pageNumber))


class EventHost(object):
    def __init__(self, editor: BookEditor):
        self.editor = editor  # 绑定editor

    def updateViewer(self):
        self.editor.update(UI_WIDGETS.contentViewText)

    def passPageEvent(self):
        printStatus('pass page event.')
        self.editor.setNextPage(UI_WIDGETS.contentViewText)
        # TODO pass age event

    def reviewPageEvent(self):
        printStatus('review page event.')
        self.editor.setLastPage(UI_WIDGETS.contentViewText)
        # TODO review page event.

    def setBookPath(self):
        """
        Set an new book.
        """
        def setNewBookPath():
            newPath = setWidgets.inputWidget.get()
            if os.path.isfile(newPath):
                printStatus(f'new path {newPath}')
                self.editor.loadBook(newPath)
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
        log(f'Going to {self.editor.getWorkDirectory()}')
        os.popen(f'start {self.editor.getWorkDirectory()}')


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


def normalDecoder(path: str):
    with open(path, 'r', encoding='utf-8') as files:
        strBook = files.read()
    log(f'Loading book {path}')
    # Load the book's text end

    print('Normal book, without and format.')
    book = Book()  # Initialize the book object.
    chapterSpliter = re.compile(r'第<\d*>章')  # Split the chapter with re.
    results = chapterSpliter.split(strBook)
    # Text manage end.

    book.addInfo('name', results[0])
    del results[0]  # Delete the first part of the book(may be it is its description)
    for chapterText in results:
        book.addChapter(chapterText)
    return book


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
    EVENT_HOST = EventHost(EDITOR)
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW, EVENT_HOST)  # 加载主窗体UI
    # initialize object end

    EDITOR.loadBook(CONFIGURE['bookPath'])  # Preload the default book.
    EVENT_HOST.updateViewer()  # Update the viewer to display the first page.

    MAIN_WINDOW.bind('<Configure>', windowConfig)  # Listening to window config event and log on status label

    # UI_WIDGETS.contentViewText.insert('insert', 'hello world')  # Initial text ,will change into an image.
    MAIN_WINDOW.mainloop()  # Calling main loop.
