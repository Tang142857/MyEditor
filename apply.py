"""
TextbookChecker
@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
import json
import tkinter
import tkinter.messagebox
import os
from time import localtime, strftime, time
import ui
import debug


class Book(object):
    def __init__(self, filePaths: str):
        """
        Initialize the book ,when TBC running the can only have one book.
        """
        printStatus('Initialize Text Book ')
        self.bookPaths = None
        self.bookOriginObject = None
        self.formatedBook = None
        self.setNewBook(filePaths)  # set the path point to the origin book

    def setNewBook(self, newPath: str):
        printStatus(f'set new book,path: {newPath}')
        try:
            self.bookOriginObject.close()  # 关闭上一本书
        except AttributeError:
            pass  # if there happen attribute error ,it maight be initialize the book,pass it.
        self.bookPaths = newPath
        self.bookOriginObject = open(self.bookPaths, encoding='utf-8')
        MAIN_WINDOW.title(f'Text Book Reader-{self.bookPaths}')

    def getNowPath(self):
        """
        Get now working book path.
        """
        return self.bookPaths

    def saveFile(self):
        pass  # TODO Saving function

    def getNextPage(self):
        newContent = self.bookOriginObject.read(20)
        return newContent
        # TODO Getting next page better

    def getNextChapter(self):
        pass  # TODO Getting next chapter


class TextBook(Book):
    """Text book is almost the same as book object ,it needn't to laod the ftb file."""
    def __init__(self, filePath: str):
        super().__init__(filePath)  # Directly using init function is OK.


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
    UI_WIDGETS.contentViewText.insert('insert', 'hello world')
    MAIN_WINDOW.mainloop()  # 调用主循环
