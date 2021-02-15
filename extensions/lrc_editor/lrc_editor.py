"""
Lrc edit extension for ME

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
from extensions import base
import tkinter
import playsound

LRC_PUNCTUATION = {
    "special_key": [],
    "key_word": [],
    "special_range": [["[", "]", True]],
    "say_signal": []
}  # need to reset the key words


def _translate(num_time):
    """Translate number time to str time"""
    minutes, remain_time = int_time // 60, int_time % 60
    str_minute, str_second = map(str, (round(minutes), round(remain_time, 2)))
    str_second = (str_second.split('.')[0].rjust(2, '0'), str_second.split('.')[1].ljust(2, '0'))
    str_time = str_minute.rjust(2, '0') + f':{str_second[0]}.{str_second[1]}'
    return str_time


class CommandBox(tkinter.Toplevel):
    def __init__(self, master, **frame_args):
        super.__init__(master, **frame_args)
        name_show=tkinter.Label(self,text='Music Name')
        play_control_frame=tkinter.Frame(self)



class LrcEditor(base.BaseExtension):
    def __init__(self, accessor):
        super().__init__(accessor)

    def on_load(self, **args):
        """重置关键词"""
        core_editor_interface = self._get_element('extension_interfaces>core_editor')
        core_editor_interface.set_signal('update', None, LRC_PUNCTUATION)

    def un_load(self):
        pass