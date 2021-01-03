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
    def makeBookName(self, Paths: str):
        """Make the formated book name."""
        baseFileName = re.split(r'[\\/]', Paths)[-1]  # To get the file name.
        fileExtendName = '.' + re.split(r'\.', baseFileName)[-1]  # To get the extend name.
        newFileName = '$' + baseFileName.replace(fileExtendName, '$' + fileExtendName)
        return Paths.replace(baseFileName, newFileName)

    def loadBook(self, path: str):
        self.originalBookPath = path
        self.formattedBookPath = self.makeBookName(path)
        self.pageNumber = 0
        self.data = normalDecoder(path=path)
        # Load book end

        MAIN_WINDOW.title('Text Book Reader-' + path)  # Reset the title of the main window.

    def setNextPage(self, viewer):
        viewer.delete(1.0, 'end')  # Delete the last page.
        viewer.insert('end', self.data.getChapter(self.pageNumber))
        self.pageNumber += 1


class EventHost(object):
    def __init__(self, editor: BookEditor):
        self.editor = editor  # 绑定book

    def passPageEvent(self):
        printStatus('pass page event.')
        self.editor.setNextPage(UI_WIDGETS.contentViewText)
        # TODO pass age event

    def reviewPageEvent(self):
        printStatus('review page event.')
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
        del pyperclip  # Clean up the memory

    def saveFile(self):
        """Save file to the formatted file."""
        printStatus('Saving file.')
        self.book.saveFile()  # Calling book object


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
    print(event)
    UI_WIDGETS.statusLabel.config(text=event.__str__())


def normalDecoder(path: str):
    with open(path, 'r', encoding='utf-8') as files:
        strBook = files.read()
    # Load the book's text end

    print('Normal book, without and format.')
    book = Book()  # Initialize the book object.
    chapterSpliter = re.compile(r'第<\d*>章')  # Split the chapter with re.
    r = chapterSpliter.split(strBook)
    # Text manage end.

    book.addInfo('name', r[0])
    del r[0]
    for chapterText in r:
        book.addChapter(chapterText)
    return book


if __name__ == "__main__":
    with open('resource/configure.json', 'r', encoding='utf-8') as configure:
        CONFIGURE = json.loads(configure.read())
        print(CONFIGURE)
    # Load configure file end.

    MAIN_WINDOW = tkinter.Tk()
    EDITOR = BookEditor()
    EDITOR.loadBook(CONFIGURE['bookPath'])
    EVENT_HOST = EventHost(EDITOR)
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW, EVENT_HOST)  # 加载主窗体UI
    # initialize object end

    printStatus(f'window geometry:{MAIN_WINDOW.geometry()}')
    MAIN_WINDOW.bind('<Configure>', windowConfig)  # Listening to window config event and log on status label
    # UI_WIDGETS.contentViewText.insert('insert', 'hello world')  # Initial text ,will change into an image.
    MAIN_WINDOW.mainloop()  # Calling main loop.
