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
    def __init__(self, data):
        self.data = data  # bind the book with editor

    def setNextPage(self, viewer):
        pass


# class TextBook(object):
#     def __init__(self, filePaths: str):
#         """Initialize the book ,when TBC running the can only have one book."""
#         printStatus('Initialize Text Book ')
#         self.bookPaths = None
#         self.bookOriginObject = None
#         self.formatedBook = None

#         self.setNewBook(filePaths)  # set the path point to the origin book

# def __makeBookName(self, Paths: str):
#     """Make the formated book name."""
#     baseFileName = re.split(r'[\\/]', Paths)[-1]
#     return Paths.replace(baseFileName, '$' + baseFileName)

#     def setNewBook(self, newPaths: str):
#         printStatus(f'set new book,path: {newPaths}')
#         try:
#             self.bookOriginObject.close()  # 关闭上一本书
#             self.formatedBook.close()
#         except AttributeError:
#             pass  # if there happen attribute error ,it maight be initialize the book,pass it.
#         # finish closing the last book

#         self.bookPaths = newPaths
#         self.bookOriginObject = open(self.bookPaths, encoding='utf-8', buffering=True)
#         self.formatedBook = open(self.__makeBookName(newPaths), 'a', encoding='utf-8',
#                                  buffering=True)  # creat formatted book name
#         MAIN_WINDOW.title(f'Text Book Reader-{self.bookPaths}')

#     def getNowPath(self):
#         """
#         Get now working book path.
#         """
#         return self.bookPaths

#     def saveFile(self):
#         self.formatedBook.flush()  # Write the content in memory to the file.

#     def getNextPage(self):
#         """Add changed content to the memory and return new content."""
#         newContent = self.bookOriginObject.read(400)

#         self.formatedBook.write(UI_WIDGETS.contentViewText.get(1.0, 'end'))  # Read the content and add to the memory
#         UI_WIDGETS.contentViewText.delete(1.0, 'end')  # Delete the remaining text.

#         return newContent
#         # TODO Getting next page better


class EventHost(object):
    def __init__(self, Book: TextBook):
        self.book = Book  # 绑定book

    def passPageEvent(self):
        printStatus('pass page event.')
        UI_WIDGETS.contentViewText.insert('insert', self.book.getNextPage())
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
                self.book.setNewBook(newPath)
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


def tUpdateXY():
    printStatus(MAIN_WINDOW.geometry(), head='window geometry:')


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
    BOOK_OBJ = TextBook(CONFIGURE['bookPath'])
    EVENT_HOST = EventHost(BOOK_OBJ)
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW, EVENT_HOST)  # 加载主窗体UI
    # initialize object end

    printStatus(f'window geometry:{MAIN_WINDOW.geometry()}')
    UI_WIDGETS.contentViewText.insert('insert', 'hello world')  # Initial text ,will change into an image.
    MAIN_WINDOW.mainloop()  # Calling main loop.
