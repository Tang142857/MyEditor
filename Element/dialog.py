"""
dialog function for apply,use 'dialog>func_name' to call or directly import Element.dialog

@author: tang142857
Copyright(c) DFSA Software Develop Center
"""

import tkinter
import tkinter.filedialog
import tkinter.ttk

COMMON = ('Microsoft YaHei', 12)
DES = ('Microsoft YaHei', 10)


class Answer(object):
    """Answer class ,to save the answer and share it with other object"""

    def __init__(self, value=None):
        self.answer_str = value

    def get(self):
        return self.answer_str

    def set(self, new_value: str):
        self.answer_str = new_value


class DescribedEntry(tkinter.Frame):
    """An entry with describe"""

    def __init__(self, master, des: str, **entry_args):
        super().__init__(master)
        self.describe_label = tkinter.Label(self, text=des, font=DES)
        self.entry = tkinter.Entry(self, **entry_args)

    def pack_(self, **args):  # 不能重名
        self.pack(**args)
        self.describe_label.pack(side='left', fill='y')
        self.entry.pack(side='left', fill='y')


class DescribedCombobox(tkinter.Frame):
    """只提供了[]运算符向combobox的传参，其他请使用object_name.choice_box.func"""

    def __init__(self, master, des: str, **combobox_args):
        super().__init__(master)
        self.describe_label = tkinter.Label(self, text=des)
        self.combobox = tkinter.ttk.Combobox(self, **combobox_args)

    def pack_(self, **args):  # 不能重名
        self.pack(**args)
        self.describe_label.pack(side='left', fill='y')
        self.combobox.pack(side='left', fill='y')

    def __getitem__(self, index):
        return self.combobox[index]

    def __setitem__(self, index, value):
        self.combobox[index] = value


class BaseDialogBox(tkinter.Toplevel):
    """Basic widgets the ask dialog box need"""

    def __init__(self, title, message, **args):
        """
        Initialize function of BaseDialogBox
        :param title: the title of the box
        :param message: message you want to show
        :param args: user_answer:Answer
        """
        super().__init__()
        self.titleName = title
        self.message = message
        self.args = {'des': 'Name:'}
        self.args.update(args)
        # create widgets
        self.message_box = tkinter.Label(self, text=self.message, font=COMMON)
        self.answer = tkinter.StringVar()
        self.entrance = DescribedEntry(self, self.args['des'], textvariable=self.answer, font=COMMON)
        self.sure_button = tkinter.Button(self, text='Sure', command=self.return_answer)
        self.cancel_button = tkinter.Button(self, text='Cancel', command=self.exit_window)
        # pack message box first,maybe you need add more widgets in it
        self.message_box.pack()

    def setup(self):
        """Setup widgets"""
        self.title(self.titleName)

        self.protocol('WM_DELETE_WINDOW', self.exit_window)
        self.entrance.pack_()
        self.sure_button.pack(side='left', padx=5)
        self.cancel_button.pack(side='left', padx=5)

        self.mainloop()

    def return_answer(self):
        """Override the function to get answer,and do not forget exit_window"""
        print(f'Default return_answer function ,answer {self.answer.get()}')
        self.exit_window()

    def exit_window(self):
        self.quit()
        self.destroy()


class AskQuestionBox(BaseDialogBox):
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)

    def return_answer(self):
        self.args['user_answer'].set(self.answer.get())
        self.exit_window()


class AskKeyValueBox(BaseDialogBox):
    def __init__(self, *arg, **args):
        """
        :param args: title: the title of the box,message: message you want to show
        user_key:Answer,user_answer:Answer
        """
        super().__init__(*arg, **args)
        self.choice_box = DescribedCombobox(self, 'Key')
        self.choice_box['values'] = self.args['choice']
        self.choice_box.pack_()

    def return_answer(self):
        key, answer_str = self.choice_box.combobox.get(), self.answer.get()
        self.args['user_key'].set(key)
        self.args['user_answer'].set(answer_str)
        self.exit_window()


def ask(title: str, message: str):
    user_answer = Answer()
    AskQuestionBox(title, message, user_answer=user_answer).setup()
    return user_answer.get()


def ask_key_value(title: str, message: str, choice: list):
    user_key, user_answer = Answer(), Answer()
    AskKeyValueBox(title, message, choice=choice, user_key=user_key, user_answer=user_answer).setup()
    return user_key.get(), user_answer.get()


def ask_extension_name():
    return ask('Load extension', 'Enter extension\'s name')


def test_():
    return ask_key_value('t', 't', ['1', '2'])


if __name__ == '__main__':
    print(ask_extension_name())
    print(test_())
