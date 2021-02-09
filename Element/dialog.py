"""
dialog function for apply,use 'dilog>func_name' to call

@author: tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.filedialog
# from typing import Callable

COMMON = ('Microsoft YaHei', 12)


class BaseDialogBox(tkinter.Toplevel):
    """Basical widgets the ask dialog box need"""
    def __init__(self, title, message, **args):
        super().__init__()
        self.titleName = title
        self.message = message
        self.args = args

    def setup(self):
        """Setup widgets"""
        self.title(self.titleName)

        self.message = tkinter.Label(self, text=self.message, font=COMMON)
        self.answer = tkinter.StringVar()
        self.entrance = tkinter.Entry(self, textvariable=self.answer, font=COMMON)
        self.okButton = tkinter.Button(self, text='Sure', command=self.returnAnswer)
        self.cancelButton = tkinter.Button(self, text='Cancel', command=self.exitWindow)

        self.protocol('WM_DELETE_WINDOW', self.exitWindow)

    def placeWidgets(self):
        """Place the widgets,you may need override this function to have a better appearance"""
        self.message.pack()
        self.entrance.pack()
        self.okButton.pack(side='left', padx=5)
        self.cancelButton.pack(side='left', padx=5)

    def returnAnswer(self):
        """Override the function to get answer"""
        return self.answer.get()

    def exitWindow(self):
        self.quit()
        self.destroy()

    def show(self):
        self.mainloop()


class AskExtensionBox(BaseDialogBox):
    def __init__(self, *arg, **args):
        """Callback normally is loadExtensions"""
        super().__init__(*arg, **args)

    def returnAnswer(self):
        self.args['callback'](name=self.answer.get())
        self.exitWindow()


def ask_extension_name():
    def getAnswer(name: str):
        global answer
        answer = name

    box = AskExtensionBox('Load extension', 'Enter extension\'s name', callback=getAnswer)
    box.setup()
    box.placeWidgets()
    box.show()
    try:
        return answer
    except NameError:
        return None


if __name__ == '__main__':
    print(ask_extension_name())
