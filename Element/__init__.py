"""
Element package of ME

@author:Tang142857
Copyright(c): DFSA Software Develop Center
"""
import json
from Element import share_memory

__all__ = ['dialog', 'main_event', 'ui']
# try load local config for apply.py
print(f'Importing element at {__file__}')

try:
    with open('Element/local.json', 'r', encoding='utf-8') as f:
        local_configure = json.loads(f.read())
    share_memory.CONFIG.update(local_configure)
except FileNotFoundError as msg:
    print(f'Load local configure file failed ,message: {msg}')
else:
    print('Load local configure file successfully.')