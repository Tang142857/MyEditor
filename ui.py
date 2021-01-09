"""
text book checker ui configure file
@author: tang142857
Copyright(c) DFSA Software Develop Center

All ui objects need father widgets,they will set ui in __init__ function
"""
import tkinter

COMMON_FONT = ('宋体', 12)
VIEWER_FONT = ('宋体', 10)
BORDER_STYLE = {'borderwidth': 4, 'relief': 'raise'}
STATUS_FONT = ('黑体', 9)
# global variable end


class MainWidgets(object):
    """
    main window's ui object
    """
    def __init__(self, tks: tkinter.Tk, EH):
        self.tks = tks
        self.eventHosts = EH
        self.tks.geometry('700x360+355+200')
        # Set window attribute end

        self.mainWindowMenu = tkinter.Menu(self.tks)
        fileMenu = tkinter.Menu(self.mainWindowMenu, tearoff=False)
        fileMenu.add_command(label='Open', command=self.eventHosts.setBookPath)
        fileMenu.add_command(label='Save', command=self.eventHosts.saveFile)
        fileMenu.add_separator()
        fileMenu.add_command(label='Copy', command=self.eventHosts.copyContent)
        fileMenu.add_command(label='Directory', command=self.eventHosts.openWorkDirectory)
        self.mainWindowMenu.add_cascade(label='File', menu=fileMenu, underline=1)
        # Menu set end

        self.mainFrame = tkinter.Frame(self.tks)
        self.displayFrame = tkinter.Frame(self.mainFrame, background='red', width=200, height=100, **BORDER_STYLE)
        self.fastWidgetsFrame = tkinter.Frame(self.mainFrame, background='green', **BORDER_STYLE)
        self.fastSettingFrame = tkinter.Frame(self.fastWidgetsFrame, background='blue', height=150, **BORDER_STYLE)
        self.statusShowFrame = tkinter.Frame(self.tks, background='yellow', height=20)
        # Frame initialize end

        self.contentViewText = tkinter.Text(self.displayFrame, font=VIEWER_FONT)
        self.passButton = tkinter.Button(self.fastWidgetsFrame,
                                         text='  Next  ',
                                         height=2,
                                         font=COMMON_FONT,
                                         command=self.eventHosts.nextPageEvent)
        self.reviewButton = tkinter.Button(self.fastWidgetsFrame,
                                           text=' Review ',
                                           height=2,
                                           font=COMMON_FONT,
                                           command=self.eventHosts.reviewPageEvent)
        self.statusLabel = tkinter.Label(self.statusShowFrame, text='Status', font=STATUS_FONT)
        # Widget initialize end
        self.applyWidgets()

    def applyWidgets(self):
        self.tks.config(menu=self.mainWindowMenu)
        # Place the menu.

        self.mainFrame.pack(side='top', fill='both', expand=True)
        self.fastWidgetsFrame.pack(side='right', fill='both')
        self.displayFrame.pack(side='left', fill='both', expand=True)
        self.statusShowFrame.pack(side='bottom', fill='x')
        # Place the frame widget.

        self.contentViewText.pack(expand=True, fill='both')
        self.reviewButton.pack(side='top', expand=True, fill='x')
        self.fastSettingFrame.pack(fill='both', expand=True)
        self.passButton.pack(side='bottom', expand=True, fill='x')
        self.statusLabel.pack(anchor='w',fill='x', expand=True)


class SetBookPathWindow(object):
    """
    set or checkout to another book function's ui object
    """
    def __init__(self, toplevels, setFunction):
        self.toplevels = toplevels
        self.toplevels.title('Set book path')
        self.chooseFrame = tkinter.Frame(toplevels)
        # set up window and frame end

        self.inputWidget = tkinter.Entry(toplevels, font=COMMON_FONT)
        self.cancelButton = tkinter.Button(self.chooseFrame, text='cancel', command=self.cancelQuit, font=COMMON_FONT)
        self.yesButton = tkinter.Button(self.chooseFrame, text='set', command=setFunction, font=COMMON_FONT)
        self.applyWidgets()

    def cancelQuit(self):
        self.toplevels.quit()
        self.toplevels.destroy()  # toplevel的玄学东西，quit之后还要加上destroy

    def applyWidgets(self):
        self.inputWidget.pack(expand=True, fill='both')
        self.chooseFrame.pack(expand=True, fill='x')
        self.yesButton.pack(expand=True, side='left', fill='y')
        self.cancelButton.pack(expand=True, side='right', fill='y')
