"""
File tree serve for ME.

@author:tang142857
copyright(c): DFSA Software Develop Center
"""
from extensions import base


class FileTree(base.BaseExtension):
    """File tree extension object."""
    def __init__(self, *arg, **args):
        super().__init__(*arg, **args)
