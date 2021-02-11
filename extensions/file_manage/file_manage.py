"""
file serve model for ME

@author: Tang142857
Copyright(c) DFSA Software Develop Center
"""
from extensions import base


class Manager(base.BaseExtension):
    """File manage serve for me editor"""

    def __init__(self, accessor):
        super(Manager, self).__init__(accessor)

    def on_load(self, **arg):
        pass

    def un_load(self):
        pass
