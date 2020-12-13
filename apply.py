"""
TextbookChecler
@author(Please add your name after this): Tang142857
Copyright(c) DFSA Software Develop Center
"""
import tkinter
from time import localtime, strftime, time


class MainWidgets(object):
    def __init__(self, tks: tkinter.Tk):
        self.tks = tks
        printStatus('Initializing the widgets...')
        self.tks.geometry('630x306+355+200')
        # Set window attribute end

        self.displayFrame = tkinter.Frame(self.tks, background='red', width=200, height=100)
        self.fastWidgetsFrame = tkinter.Frame(self.tks, background='green', width=100, height=100)
        # Frame initialize end

        # Widget initialize start
        self.passButton = tkinter.Button(self.fastWidgetsFrame,
                                         text='pass',
                                         height=1,
                                         command=tUpdateXY,
                                         font=('microsoftyamei', 10))
        self.applyWidgets()

    def applyWidgets(self):
        printStatus('apply widgets...')
        self.displayFrame.pack(side='left', fill='both')
        self.fastWidgetsFrame.pack(side='right', fill='both')
        self.passButton.pack(side='bottom')


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
    printStatus(MAIN_WINDOW.geometry(),head='window geometry:')


if __name__ == "__main__":
    MAIN_WINDOW = tkinter.Tk()
    UI_WIDGETS = MainWidgets(MAIN_WINDOW)
    print(MAIN_WINDOW.geometry())
    MAIN_WINDOW.mainloop()  # 调用主循环
