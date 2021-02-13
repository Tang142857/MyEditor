"""
Lrc edit extension for ME

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
from extensions import base


class LrcEditor(base.BaseExtension):
    def __init__(self, accessor):
        super().__init__(accessor)

    def on_load(self, **args):
        """"""
        pass  # TODO lrc extension on load

    def un_load(self):
        pass