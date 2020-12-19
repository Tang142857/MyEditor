"""
TextbookChecker
@author(Please add your name after this): Tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
from time import localtime, strftime, time
import ui


class TextBook(object):
    def __init__(self, filePaths):
        printStatus('Initialize Text Book ')
        self.bookPaths = filePaths  # 文件位置，TBC的保存不是时时的，只在调用save时保存
        self.bookOriginObject = open(self.bookPaths, encoding='utf-8')

    def saveFile(self):
        pass  # TODO Saving function

    def getNextChapter(self):
        pass  # TODO Getting next chapter

    def getNextPage(self):
        pass  # TODO Getting next page


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
    UI_WIDGETS = ui.MainWidgets(MAIN_WINDOW)
    # print(MAIN_WINDOW.geometry())
    MAIN_WINDOW.mainloop()  # 调用主循环
