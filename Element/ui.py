"""
UI widgets for main apply

@author: Tang142857
@file: ui.py ,Create at: 2021-02-14
Copyright(c): DFSA Software Develop Center
"""
import tkinter
import tkinter.scrolledtext

try:
    from Element import main_event, share_memory
except ImportError:  # to test the model only
    import main_event


class MainWidgets(object):
    """
    main window's ui object
    """
    def __initEvents__(self):
        """Initialize all events."""
        self.copyContentEvent = main_event.CopyContentEvent()
        self.loadExtensionsEvent = main_event.LoadExtensionsEvent()

    def __init__(self, windows: tkinter.Tk):
        self.__initEvents__()
        self.windows = windows
        self.windows.geometry(share_memory.CONFIG['window_config']['position'])
        self.windows.title(share_memory.CONFIG['window_config']['init_title'])
        # Set window attribute end

        self.mainWindowMenu = tkinter.Menu(self.windows)

        self.fileMenu = tkinter.Menu(self.mainWindowMenu, tearoff=False)
        self.fileMenu.add_command(label='Copy Content', command=self.copyContentEvent.emit)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Manage Extension', command=self.loadExtensionsEvent.emit)

        self.mainWindowMenu.add_cascade(label='File', menu=self.fileMenu, underline=1)
        # Menu set end

        self.x_structure = tkinter.PanedWindow(self.windows, background='red')
        # self.mainFrame = tkinter.Frame(self.windows)
        self.displayFrame = tkinter.Frame(self.x_structure, width=200, height=50)
        self.statusShowFrame = tkinter.Frame(self.windows, background=share_memory.CONFIG['light_blue'], height=12)
        self.toolBarFrame = tkinter.Frame(self.x_structure, background='green', width=30)
        # Frame initialize end

        self.textViewer = tkinter.scrolledtext.ScrolledText(self.displayFrame, font=share_memory.CONFIG['viewer_font'])
        self.statusLabel = tkinter.Label(self.statusShowFrame,
                                         text='Status',
                                         font=share_memory.CONFIG['status_font'],
                                         anchor='w',
                                         background='#007ACC')
        self.fillEmptyLabel = tkinter.Label(self.displayFrame,
                                            font=share_memory.CONFIG['fill_text_font'])  # A label to fill text
        # Widget initialize end
        self.applyWidgets()

    def applyWidgets(self):
        self.windows.config(menu=self.mainWindowMenu)
        # Place the menu.

        self.statusShowFrame.pack(side='bottom', fill='x')
        self.x_structure.add(self.toolBarFrame)
        self.x_structure.add(self.displayFrame)

        # self.displayFrame.pack(side='left', fill='both', expand=True)
        # Place the frame widget.

        self.x_structure.pack(fill='both', expand=True)
        self.textViewer.pack(expand=True, fill='both')
        self.statusLabel.pack(side='left', fill='y')

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
