"""
TextbookChecker
@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.messagebox
import os
from time import localtime, strftime, time
import ui
import debug


class TextBook(object):
    def __init__(self, filePaths: str):
        printStatus('Initialize Text Book ')
        self.setNewBook(filePaths)
        # self.bookPaths = filePaths  # 文件位置，TBC的保存不是时时的，只在调用save时保存
        # self.bookOriginObject = open(self.bookPaths, encoding='utf-8')

    def setNewBook(self, newPath: str):
        printStatus(f'set new book,path: {newPath}')
        try:
            self.bookOriginObject.close()  # 关闭上一本书
        except AttributeError:
            pass
        self.bookPaths = newPath
        self.bookOriginObject = open(self.bookPaths, encoding='utf-8')
        MAIN_WINDOW.title(f'Text Book Reader-{self.bookPaths}')

    def getNowPath(self):
        """
        提供给set方法的状态读取函数
        """
        printStatus('get book path.')
        return self.bookPaths

    def saveFile(self):
        pass  # TODO Saving function

    def getNextPage(self):
        newContent = self.bookOriginObject.read(20)
        return newContent
        # TODO Getting next page better

    def getNextChapter(self):
        pass  # TODO Getting next chapter


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
        nowContent = UI_WIDGETS.contentViewText.get(1.0,'end')
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
    MAIN_WINDOW = tkinter.Tk()
    BOOK_OBJ = TextBook('D:\\relaxing\\factions\\countryside_teacher\\ct.txt')
    EVENT_HOST = EventHost(BOOK_OBJ)
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW, EVENT_HOST)  # 加载主窗体UI
    # initialize object end

    printStatus(f'window geometry:{MAIN_WINDOW.geometry()}')
    UI_WIDGETS.contentViewText.insert('insert', 'hello world')
    MAIN_WINDOW.mainloop()  # 调用主循环
