"""
dialog function for apply,use 'dilog>func_name' to call

@author: tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.filedialog
from typing import Callable

COMMON = ('Microsoft YaHei', 12)


class ExitException(Exception):
    def __init__(self, answer):
        self.answer = answer


def _ask(master, title: str, message: str, callback: Callable, **args):
    """Ask a question and get answer."""
    def getAnwser():
        callback(answer.get())
        root.destroy()

    root = tkinter.Toplevel(master=master)

    message = tkinter.Label(root, text=message, font=COMMON)
    answer = tkinter.StringVar()
    entrance = tkinter.Entry(root, textvariable=answer, font=COMMON)
    okButton = tkinter.Button(root, text='Sure', command=getAnwser)
    cancelButton = tkinter.Button(root, text='Cancel', command=root.destroy)

    message.pack()
    entrance.pack()
    okButton.pack()
    cancelButton.pack()

    root.mainloop()
    return ret


def do():
    _ask(win, 'test', 'test', r)


def r(ans):
    print(ans)


if __name__ == '__main__':
    win = tkinter.Tk()
    b = tkinter.Button(win, text='test', command=do)
    b.pack()
    win.mainloop()