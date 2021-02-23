"""
BullshitGenerator extension for ME

@author: Reproduce by Tang142857
@project: MyEditor
@file: maker.py
@date: 2021-02-23
"""
import os
import random
import re
import json
import tkinter
from extensions import base
from Element import main_event

with open('extensions/litter_maker/data.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

famous_saying = data["famous"]  # a 代表前面垫话，b代表后面垫话
foreground_saying = data["before"]  # 在名人名言前面弄点废话
background_saying = data['after']  # 在名人名言后面弄点废话
litter = data['bosh']  # 代表文章主要废话来源


def shuffle_list(l):
    global repeat_index
    saying_pool = list(l) * 2
    while True:
        random.shuffle(saying_pool)
        for element in saying_pool:
            yield element


next_sentence = shuffle_list(litter)
next_famous_saying = shuffle_list(famous_saying)


def get_famous_saying():
    global next_famous_saying
    result = next(next_famous_saying)
    result = result.replace("a", random.choice(foreground_saying))
    result = result.replace("b", random.choice(background_saying))
    return result


def new_passage():
    result = "\n"
    return result


def make(topic):
    """
    Make a litter ,main function of litter maker.
    """
    full_content = str()

    for x in topic:
        # I don't know why origin editor write this ,maybe only get more context
        tmp = str()  # new part
        while (len(tmp) < 6000):
            branch = random.randint(0, 100)
            # To let the context random :)
            if branch < 5:
                tmp += new_passage()
            elif branch < 20:
                tmp += get_famous_saying()
            else:
                tmp += next(next_sentence)
        # get the origin context ,replace the white space to topic
        tmp = tmp.replace("x", topic)
        full_content += tmp  # add this part to content

    return full_content


# litter make functions end here
# thanks for the origin author's support
# ME extension codes begin from here


class MakerFrame(tkinter.Frame):
    """The console frame of litter maker."""
    def __init__(self, master, **frame_args):
        super().__init__(master, **frame_args)

        self.topic_var = tkinter.StringVar(self)
        self.topic_input = tkinter.Entry(self, textvariable=self.topic_var)
        self.make_event = main_event.Event()
        self.start_make = tkinter.Button(self, text='Make', command=self.make_event.emit)

    def get_topic(self):
        return self.topic_var.get()

    def pack(self, **frame_args):
        tkinter.Frame.pack(self, **frame_args)

        self.topic_input.pack(fill='x')
        self.start_make.pack()


class Maker(base.BaseExtension):
    def __init__(self, accessor):
        super().__init__(accessor)

    def on_load(self, **args):
        """Insert consol frame ,bind events"""
        ui = self._get_element('UI_WIDGETS')
        self._console = MakerFrame(ui.toolBarFrame)
        self._console.pack(fill='x')

        self._console.make_event.add_callback(self.make_litter)

    def un_load(self):
        """带来的都带走"""
        self._console.destroy()

    # ####### extension requirements end here ,public function start here #######
    def make_litter(self, event=None):
        """Get topic ,make litter ,insert into text ,check"""
        topic = self._console.get_topic()
        content = make(topic)

        ui = self._get_element('UI_WIDGETS>textViewer')
        ui.insert('insert', content)

        self._get_element('extension_interfaces>core_editor>check')()


if __name__ == "__main__":
    t = make('git')
    print(t)