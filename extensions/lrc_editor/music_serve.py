"""
Music information serve for lrc editor

@author: Tang142857
@file: music_serve.py ,Create at: 2021-02-15
Copyright(c): DFSA Software Develop Center
"""
import os
import wave
import pyaudio
import tkinter.messagebox
import threading

from time import sleep


class PlayError(Exception):
    def __init__(self, time_code, message):
        self.time_code = time_code
        self.message = message


class Music(threading.Thread):
    STOP_FLAG = False

    def __init__(self, path: str, callback=None):
        assert os.path.isfile(path), 'Not a file'

        super().__init__()

        ext_name = path.split('.')[-1]
        if ext_name == 'wav':
            self._load_file(path)
        else:  # translate to other format to wave
            from subprocess import call
            new_flie_name = '.'.join(path.split('.')[:-1]) + '.wav'
            command = f'ffmpeg -i {path} {new_flie_name}'
            return_code = call(command, shell=True)
            if return_code != 0:
                tkinter.messagebox.showerror('Music open wrong',
                                             'FFmpeg can not decode the file,please change it to wav by yourself.')
            self._load_file(new_flie_name)
        self.callback = callback

    def _load_file(self, path):
        self.wave_file = wave.open(path, 'rb')
        self.audio = pyaudio.PyAudio()
        self.output_stream = self.audio.open(format=self.audio.get_format_from_width(self.wave_file.getsampwidth()),
                                             channels=self.wave_file.getnchannels(),
                                             rate=self.wave_file.getframerate(),
                                             output=True)

    def play_async(self, step_length=1024):
        self.STOP_FLAG = False
        # move the pointer to proper position

        while frame := self.wave_file.readframes(step_length):
            self.output_stream.write(frame)
            if self.STOP_FLAG: return
        self.wave_file.setpos(0)  # 指针归位

    def stop(self):
        self.STOP_FLAG = True

    def run(self, *arg, **args):
        self.play_async(*arg, **args)
        if self.callback is not None: self.callback()
        super().__init__()

    def get_time(self):
        time = self.wave_file.tell() / self.wave_file.getframerate()
        return round(time, 2)

    def close(self):
        self.output_stream.stop_stream()
        self.wave_file.close()
        self.output_stream.close()
        self.audio.terminate()


if __name__ == '__main__':
    import time
    m = Music('E:/PY/base_test/program_1/test_sound.wav')
    m.start()
    time.sleep(3)
    m.stop()
    time.sleep(2)
    m.start()
    time.sleep(40)
    m.start()
    m.close()
