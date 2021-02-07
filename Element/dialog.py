"""
dialog function for apply,use 'dilog>func_name' to call

@author: tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.filedialog

COMMON = ('Microsoft YaHei', 12)


def _ask(master, title: str, message: str, **args):
    root = tkinter.Toplevel(master=master)

    message = tkinter.Label(root, text=message, font=COMMON)
    answer = tkinter.StringVar()
    entrance = tkinter.Entry(root, textvariable=answer, font=COMMON)
    okButton = tkinter.Button(root, text='Sure', command=None)
    cancelButton = tkinter.Button(root, text='Cancel', command=None)

    message.pack()
    entrance.pack()
    okButton.pack()
    cancelButton.pack()

    root.mainloop()


if __name__ == '__main__':
    _ask(None, 'test', 'test')
