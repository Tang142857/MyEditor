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


class Music(threading.Thread):
    STOP_FLAG = False

    def __init__(self, path: str):
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

    def _load_file(self, path):
        self.wave_file = wave.open(path, 'rb')
        self.audio = pyaudio.PyAudio()
        self.output_stream = self.audio.open(format=self.audio.get_format_from_width(self.wave_file.getsampwidth()),
                                             channels=self.wave_file.getnchannels(),
                                             rate=self.wave_file.getframerate(),
                                             output=True)
        self.pointer = 0

    def play_async(self, step_length=1024, continue_=False):
        self.STOP_FLAG=False
        if continue_: self.pointer = 0
        frame = self.wave_file.readframes(self.pointer)
        # move the pointer to proper position

        while frame := self.wave_file.readframes(step_length):
            self.output_stream.write(frame)
            self.pointer += step_length
            if self.STOP_FLAG: return
    
    def stop(self):
        self.STOP_FLAG=True

    def run(self, *arg, **args):
        self.play_async(*arg, **args)
        super().__init__()

    def close(self):
        self.output_stream.stop_stream()
        self.wave_file.close()
        self.output_stream.close()
        self.audio.terminate()


if __name__ == '__main__':
    import time
    m = Music('E:/PY/base_test/scrLet.wav')
    m.start()
    time.sleep(3)
    m.stop()
    time.sleep(2)
    m.start()
    time.sleep(5)
    m.close()
