"""
text book checker ui configure file
@author: tang142857
Copyright(c) DFSA Software Develop Center

All ui objects need father widgets,they will set ui in __init__ function
"""
import tkinter
import tkinter.scrolledtext

try:
    from Element import mainEvent
except ImportError:  # to test the model only
    import mainEvent

COMMON_FONT = ('宋体', 12)
VIEWER_FONT = ('consolas', 11)
BORDER_STYLE = {'borderwidth': 4, 'relief': 'raise'}
STATUS_FONT = ('Microsoft YaHei', 9)
FILL_TEXT_FONT = ('Microsoft YaHei', 50)

WINDOWS_CONFIG = {'position': '700x360+355+200', 'init_title': 'Text Book Checker'}
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
        self.closeFileEvent = mainEvent.CloseFileEvent()
        self.loadExtensionsEvent = mainEvent.LoadExtensionsEvent()

    def __init__(self, windows: tkinter.Tk):
        self.__initEvents__()
        self.windows = windows
        self.windows.geometry(WINDOWS_CONFIG['position'])
        self.windows.title(WINDOWS_CONFIG['init_title'])
        # Set window attribute end

        self.mainWindowMenu = tkinter.Menu(self.windows)

        fileMenu = tkinter.Menu(self.mainWindowMenu, tearoff=False)
        fileMenu.add_command(label='Open', command=self.openEvent.emit)
        fileMenu.add_command(label='Save', command=self.saveEvent.emit)
        fileMenu.add_command(label='Close file', command=self.closeFileEvent.emit)
        fileMenu.add_separator()
        fileMenu.add_command(label='Copy', command=self.copyContentEvent.emit)
        fileMenu.add_command(label='Directory', command=self.openWorkDirEvent.emit)
        fileMenu.add_separator()
        fileMenu.add_command(label='Extension', command=self.loadExtensionsEvent.emit)

        self.mainWindowMenu.add_cascade(label='File', menu=fileMenu, underline=1)
        # Menu set end

        self.mainFrame = tkinter.Frame(self.windows)
        self.displayFrame = tkinter.Frame(self.mainFrame, background='red', width=200, height=50, **BORDER_STYLE)
        self.statusShowFrame = tkinter.Frame(self.windows, background='blue', height=15)
        self.toolBarFrame = tkinter.Frame(self.windows, background='green', width=30)
        # Frame initialize end

        self.textViewer = tkinter.scrolledtext.ScrolledText(self.displayFrame, font=VIEWER_FONT)
        self.statusLabel = tkinter.Label(self.statusShowFrame, text='Status', font=STATUS_FONT, anchor='w')
        self.fillEmptyLabel = tkinter.Label(self.displayFrame, font=FILL_TEXT_FONT)  # A label to fill text
        # Widget initialize end
        self.applyWidgets()

    def applyWidgets(self):
        self.windows.config(menu=self.mainWindowMenu)
        # Place the menu.

        self.statusShowFrame.pack(side='bottom', fill='x')
        self.toolBarFrame.pack(side='left', fill='y')

        self.mainFrame.pack(side='top', fill='both', expand=True)
        self.displayFrame.pack(side='left', fill='both', expand=True)
        # Place the frame widget.

        self.textViewer.pack(expand=True, fill='both')
        self.statusLabel.pack(anchor='w', fill='x', expand=True)

    def fillEmptyText(self, string='No File'):
        """Fill the content view text with a big label with string."""
        self.textViewer.pack_forget()  # 先把原来的忘掉
        self.fillEmptyLabel.config(text=string)
        self.fillEmptyLabel.pack(fill='both', expand=True)  # 把填充物放上去

    def relieveEmptyText(self):
        """Delete the label that fill the empty text"""
        self.fillEmptyLabel.pack_forget()  # 忘记填充物
        self.textViewer.pack(expand=True, fill='both')


if __name__ == '__main__':
    testWindow = tkinter.Tk()
    ui = MainWidgets(testWindow)
    ui.fillEmptyText('Test')
    # res = ui.askQuestion('test', 'test')
    testWindow.mainloop()
