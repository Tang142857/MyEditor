"""
text book checker ui configure file
@author: tang142857
Copyright(c) DFSA Software Develop Center
"""
import tkinter
# from time import localtime, strftime, time

# def printStatus(values, end='\n', head=''):
#     """
#     Print the value with time string and status string.
#     :param head: sting head just like \r
#     :param end: string end just like \n
#     :param values: value
#     :return: nothing
#     """
#     originTime = localtime(time())  # 创建本地时间
#     time_string = strftime('%H:%M:%S', originTime)  # 生成时间戳
#     print(f'{head}INFO:{time_string} :: {values}', end=end)


class MainWidgets(object):
    def __init__(self, tks: tkinter.Tk):
        self.tks = tks
        self.tks.geometry('630x306+355+200')
        # Set window attribute end

        self.displayFrame = tkinter.Frame(self.tks, background='red', width=200, height=100)
        self.fastWidgetsFrame = tkinter.Frame(self.tks, background='green', width=100, height=100)
        # Frame initialize end

        # Widget initialize start
        self.passButton = tkinter.Button(self.fastWidgetsFrame, text=' pass ', height=2, font=('microsoftyamei', 10))
        self.reviewButton = tkinter.Button(self.fastWidgetsFrame,text='review',height=2,font=('microsoftyamei', 10))
        self.applyWidgets()

    def applyWidgets(self):
        self.displayFrame.pack(side='left', fill='both')
        self.fastWidgetsFrame.pack(side='right', fill='both')
        self.passButton.pack(side='bottom')
        self.reviewButton.pack(side='top')