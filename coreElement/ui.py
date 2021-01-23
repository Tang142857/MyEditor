"""
text book checker ui configure file
@author: tang142857
Copyright(c) DFSA Software Develop Center

All ui objects need father widgets,they will set ui in __init__ function
"""
import tkinter

try:
    from . import mainEvent
except ImportError:  # to test the model only
    import mainEvent

COMMON_FONT = ('宋体', 12)
VIEWER_FONT = ('宋体', 10)
BORDER_STYLE = {'borderwidth': 4, 'relief': 'raise'}
STATUS_FONT = ('Microsoft YaHei', 9)
# global variable end


class MainWidgets(object):
    """
    main window's ui object
    """
    def __initEvents__(self):
        """Initialize all events."""
        self.openWorkDirEvent = mainEvent.OpenWorkDirEvent()
        self.openEvent = mainEvent.OpenEvent()
        self.saveEvent = mainEvent.SaveEvent()
        self.copyContentEvent = mainEvent.CopyContentEvent()

    def __init__(self, tks: tkinter.Tk):
        self.__initEvents__()
        self.tks = tks
        self.tks.geometry('700x360+355+200')
        # Set window attribute end

        self.mainWindowMenu = tkinter.Menu(self.tks)
        fileMenu = tkinter.Menu(self.mainWindowMenu, tearoff=False)
        fileMenu.add_command(label='Open', command=self.openEvent.emit)
        fileMenu.add_command(label='Save', command=self.saveEvent.emit)
        fileMenu.add_separator()
        fileMenu.add_command(label='Copy', command=self.copyContentEvent.emit)
        fileMenu.add_command(label='Directory', command=self.openWorkDirEvent.emit)
        self.mainWindowMenu.add_cascade(label='File', menu=fileMenu, underline=1)
        # Menu set end

        self.mainFrame = tkinter.Frame(self.tks)
        self.displayFrame = tkinter.Frame(self.mainFrame, background='red', width=200, height=100, **BORDER_STYLE)
        self.statusShowFrame = tkinter.Frame(self.tks, background='yellow', height=20)
        # Frame initialize end

        self.contentViewText = tkinter.Text(self.displayFrame, font=VIEWER_FONT)
        self.statusLabel = tkinter.Label(self.statusShowFrame, text='Status', font=STATUS_FONT, anchor='w')
        # Widget initialize end
        self.applyWidgets()

    def applyWidgets(self):
        self.tks.config(menu=self.mainWindowMenu)
        # Place the menu.

        self.mainFrame.pack(side='top', fill='both', expand=True)
        self.displayFrame.pack(side='left', fill='both', expand=True)
        self.statusShowFrame.pack(side='bottom', fill='x')
        # Place the frame widget.

        self.contentViewText.pack(expand=True, fill='both')
        self.statusLabel.pack(anchor='w', fill='x', expand=True)


# class SetBookPathWindow(object):
#     """
#     set or checkout to another book function's ui object
#     """
#     def __init__(self, toplevels, setFunction):
#         self.toplevels = toplevels
#         self.toplevels.title('Set book path')
#         self.chooseFrame = tkinter.Frame(toplevels)
#         # set up window and frame end

#         self.inputWidget = tkinter.Entry(toplevels, font=COMMON_FONT)
#         self.cancelButton = tkinter.Button(self.chooseFrame, text='cancel', command=self.cancelQuit, font=COMMON_FONT)
#         self.yesButton = tkinter.Button(self.chooseFrame, text='set', command=setFunction, font=COMMON_FONT)
#         self.applyWidgets()

#     def cancelQuit(self):
#         self.toplevels.quit()
#         self.toplevels.destroy()  # toplevel的玄学东西，quit之后还要加上destroy

#     def applyWidgets(self):
#         self.inputWidget.pack(expand=True, fill='both')
#         self.chooseFrame.pack(expand=True, fill='x')
#         self.yesButton.pack(expand=True, side='left', fill='y')
#         self.cancelButton.pack(expand=True, side='right', fill='y')
if __name__ == '__main__':
    testWindow = tkinter.Tk()
    ui = MainWidgets(testWindow)
    testWindow.mainloop()
