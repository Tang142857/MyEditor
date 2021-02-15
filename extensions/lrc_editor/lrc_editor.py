"""
Lrc edit extension for ME

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
import tkinter
import tkinter.filedialog
import tkinter.messagebox

from extensions import base
from extensions.lrc_editor import music_serve
from extensions.core_editor.editor import _color
from Element import main_event

LRC_PUNCTUATION = {
    "special_key": [],
    "key_word": [],
    "special_range": [["[", "]", True]],
    "say_signal": []
}  # need to reset the key words


class Tag(object):
    def __init__(self, master: tkinter.scrolledtext, lint):
        self.row_number = 1
        self.master = master
        self.lint = lint
        self.master.tag_config('selected', background='yellow')

    def up_row(self, event=None):
        if self.row_number - 1 > 0:
            self.row_number -= 1
        last_row_number = self.row_number + 1
        self.lint(row_index=last_row_number - 1)
        self._update_color()

    def down_row(self, event=None):
        if self.row_number + 1 < len(self.master.get('1.0', 'end').split('\n')):
            self.row_number += 1
        last_row_number = self.row_number - 1
        self.lint(row_index=last_row_number - 1)
        self._update_color()

    def _update_color(self):
        content = self.master.get('1.0', 'end').split('\n')[self.row_number - 1]
        bracket_end_mark = content.find(']') + 1
        area_length = len(content) - bracket_end_mark
        _color((self.row_number - 1, bracket_end_mark, area_length), 'selected')


def _translate(num_time):
    """Translate number time to str time"""
    minutes, remain_time = int_time // 60, int_time % 60
    str_minute, str_second = map(str, (round(minutes), round(remain_time, 2)))
    str_second = (str_second.split('.')[0].rjust(2, '0'), str_second.split('.')[1].ljust(2, '0'))
    str_time = str_minute.rjust(2, '0') + f':{str_second[0]}.{str_second[1]}'
    return str_time


class CommandBox(tkinter.Toplevel):
    def __init__(self, master, **frame_args):
        super().__init__(master, **frame_args)
        self.title('Lyrics extension terminal.')

        self.stop_play_event = main_event.Event()
        self.start_play_event = main_event.Event()
        self.add_tag_event = main_event.Event()
        self.up_select_tag_event = main_event.Event()
        self.down_select_tag_event = main_event.Event()
        self.choose_music_event = main_event.Event()

        self.name_show = tkinter.Label(self, text='Music Name')

        self.play_control_frame = tkinter.Frame(self)
        self.start_play_button = tkinter.Button(self.play_control_frame,
                                                text='Start',
                                                command=self.start_play_event.emit)
        self.stop_play_button = tkinter.Button(self.play_control_frame, text='Stop', command=self.stop_play_event.emit)
        self.ask_pattern = tkinter.Checkbutton(self.play_control_frame, text='Create new line.')

        self.tag_control = tkinter.Frame(self)
        self.add_tag_button = tkinter.Button(self.tag_control, text='Add tag', command=self.add_tag_event.emit)
        self.up_tag_button = tkinter.Button(self.tag_control, text='Up', command=self.up_select_tag_event.emit)
        self.down_tag_button = tkinter.Button(self.tag_control, text='Down', command=self.down_select_tag_event.emit)

        self.name_show.bind('<Button-1>', self.choose_music_event.emit)
        self.ask_pattern.select()

        # self.protocol('WM_DELETE_WINDOW', tkinter.messagebox.showwarning)
        self._pack()

    def _pack(self):
        self.name_show.pack(side='top', fill='x')
        self.play_control_frame.pack()
        self.start_play_button.pack(side='left')
        self.stop_play_button.pack(side='left')
        self.ask_pattern.pack(side='left')
        self.tag_control.pack(fill='x')
        self.up_tag_button.pack(side='left')
        self.down_tag_button.pack(side='left')
        self.add_tag_button.pack(side='left', fill='x', expand=True)


class LrcEditor(base.BaseExtension):
    def __init__(self, accessor):
        super().__init__(accessor)
        self.music_file = None

    def on_load(self, **args):
        """重置关键词"""
        core_editor_interface = self._get_element('extension_interfaces>core_editor')
        core_editor_interface.set_signal('update', None, LRC_PUNCTUATION)
        # reset the key words ,end
        self.tag = Tag(self._get_element('UI_WIDGETS>textViewer'),
                       self._get_element('extension_interfaces>core_editor>check'))

        self.terminal = CommandBox(self._get_element('MAIN_WINDOW'))
        # Toplevel widget can not call mainloop,I don't know why,but if you call,there will be something wrong
        self.terminal.choose_music_event.add_callback(self._choose_music)
        self.terminal.start_play_event.add_callback(self._start_play)
        self.terminal.stop_play_event.add_callback(self._stop_play)
        self.terminal.up_select_tag_event.add_callback(self.tag.up_row)
        self.terminal.down_select_tag_event.add_callback(self.tag.down_row)

    def un_load(self):
        pass

    # ################## base function end ##################
    # following are protected function

    def _choose_music(self, event=None):
        file_path = tkinter.filedialog.askopenfilename()
        if not bool(file_path): return
        self.music_file = music_serve.Music(file_path, self._release_button)
        self.terminal.name_show.config(text=file_path)

    def _start_play(self, event=None):
        try:
            self.music_file.start()
        except AttributeError:
            tkinter.messagebox.showwarning('warning', 'Please choose a song first.\n请先选择一首歌')
        else:
            self.terminal.start_play_button.config(state='disabled')
            self.terminal.stop_play_button.config(state='normal')

    def _stop_play(self, event=None):
        try:
            self.music_file.stop()
        except AttributeError:
            tkinter.messagebox.showwarning('warning', 'Please choose a song first.\n请先选择一首歌')
        else:
            self.terminal.stop_play_button.config(state='disabled')
            self.terminal.start_play_button.config(state='normal')

    def _release_button(self):
        self.terminal.stop_play_button.config(state='normal')
        self.terminal.start_play_button.config(state='normal')
