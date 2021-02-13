"""
dialog function for apply,use 'dilog>func_name' to call or diectly import Element.dialog

@author: tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.filedialog
import tkinter.ttk
# from typing import Callable

COMMON = ('Microsoft YaHei', 12)
DES = ('Microsoft YaHei', 10)


class DescribedEntry(tkinter.Frame):
    """An entry with describ"""
    def __init__(self, master, des: str, **entry_args):
        super().__init__(master)
        self.describ_label = tkinter.Label(self, text=des, font=DES)
        self.entry = tkinter.Entry(self, **entry_args)

    def pack_(self, **args):  # 不能重名
        self.pack(**args)
        self.describ_label.pack(side='left', fill='y')
        self.entry.pack(side='left', fill='y')


class DescribedCombobox(tkinter.Frame):
    """只提供了[]运算符向combobox的传参，其他请使用object_name.combobox.func"""
    def __init__(self, master, des: str, **combobox_args):
        super().__init__(master)
        self.describ_label = tkinter.Label(self, text=des)
        self.combobox = tkinter.ttk.Combobox(self, **combobox_args)

    def pack_(self, **args):  # 不能重名
        self.pack(**args)
        self.describ_label.pack(side='left', fill='y')
        self.combobox.pack(side='left', fill='y')

    def __getitem__(self, index):
        return self.combobox[index]

    def __setitem__(self, index, value):
        self.combobox[index] = value


class BaseDialogBox(tkinter.Toplevel):
    """Basical widgets the ask dialog box need"""
    def __init__(self, title, message, **args):
        super().__init__()
        self.titleName = title
        self.message = message
        self.args = {'des': 'name:'}

        self.args.update(args)

    def setup(self):
        """Setup widgets"""
        self.title(self.titleName)

        self.message = tkinter.Label(self, text=self.message, font=COMMON)
        self.answer = tkinter.StringVar()
        self.entrance = DescribedEntry(self, self.args['des'], textvariable=self.answer, font=COMMON)
        self.okButton = tkinter.Button(self, text='Sure', command=self.return_answer)
        self.cancelButton = tkinter.Button(self, text='Cancel', command=self.exit_window)

        self.message.pack()

        self.protocol('WM_DELETE_WINDOW', self.exit_window)
        self.__place_widgets()
        self._show()

    def __place_widgets(self):
        """Place the widgets,you may need override this function to have a better appearance"""
        self.entrance.pack_()
        self.okButton.pack(side='left', padx=5)
        self.cancelButton.pack(side='left', padx=5)

    def _show(self):
        self.mainloop()

    def return_answer(self):
        """Override the function to get answer"""
        return self.answer.get()

    def exit_window(self):
        self.quit()
        self.destroy()


class AskQuestionBox(BaseDialogBox):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)

    def return_answer(self):
        self.args['callback'](name=self.answer.get())
        self.exit_window()


class AskKeyValueBox(BaseDialogBox):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
        self.combobox = DescribedCombobox(self, 'Key')
        self.combobox['values'] = self.args['choice']

    def return_answer(self):
        pass

    def __place_widgets(self):
        self.combobox.pack_()
        self._Class__place_widgets()


def ask(title: str, message: str):
    def get_answer(name: str):
        global answer
        answer = name

    AskQuestionBox(title, message, callback=get_answer).setup()
    try:
        return answer
    except NameError:
        return None


def ask_key_value(title: str, message: str, choice: list):
    def get_answer(key_, value_):
        global key, value
        key, value = key_, value_

    AskKeyValueBox(title, message, choice=choice).setup()

    try:
        return key, value
    except NameError:
        return None, None


def ask_extension_name():
    return ask('Load extension', 'Enter extension\'s name')


def test_KV():
    return ask_key_value('t', 't', ['1', '2'])


if __name__ == '__main__':
    print(ask_extension_name())
    print(test_KV())
