"""
code editor for MyEditor
@author: tang142857
Copyright(c) DFSA Software Develop Center

主编辑器函数，提供 关键字高亮，缩进增强，搜索字符串 等服务
在每次释放键盘<key-release>后都执行，尽可能小
后期支持自定义关键字

TBC extend standard
都保证包含了：initialize（初始化插件）
"""
import json
import re
import time

from extensions import base

from coreEditor import findTool

PUNCTUATION = {
    "special_key": ["a", "#", "小说", "·", "：", ":", "电子书"],
    "key_word": [],
    "special_range": [["'", "'", False], ["\"", "\"", False], ["[", "]", True]],
    "say_signal": [["“", "”", True], ["‘", "’", True]]
}

try:
    with open('coreEditor/local.json', 'r', encoding='utf-8') as config:
        localConfig = json.loads(config.read())
except FileNotFoundError as msg:
    print(f'Config not found at editor{msg}')
else:
    PUNCTUATION.update(localConfig)

# ui args start,all name with SELF_... ，用户UI，发射事件的时候是只有event的，提前储存“指针”
SELF_MW = None
SELF_UI = None
SELF_MC = {}  # 核心调用 e.g. openFile


def _color(positionList: list, kind: str):
    """
    color the string with marks.\n
    required arguments:positionList[row,startindex,length],kind: mark name
    attention: all argments use index(start at 0)!!!
    """
    rowIndex = positionList[0]
    startIndex = positionList[1]
    length = positionList[2]
    # get arguments

    _str = SELF_UI.textViewer.get(f'{rowIndex+1}.{startIndex}', f'{rowIndex+1}.{startIndex+length}')
    # get text before deleting it,for insert it again
    SELF_UI.textViewer.delete(f'{rowIndex+1}.{startIndex}', f'{rowIndex+1}.{startIndex+length}')
    # delete the string in text before
    SELF_UI.textViewer.insert(f'{rowIndex+1}.{startIndex}', _str, kind)


    # insert it again
def _scanRow(rowIndex: int, string: str):
    """
    Scan the row and color words.Use public interface needn't other arguments.
    """
    # update the row first to clean the outdate marks off
    SELF_UI.textViewer.delete(f'{rowIndex+1}.0', f'{rowIndex+1}.{len(string)}')
    SELF_UI.textViewer.insert(f'{rowIndex+1}.0', string)

    # 特殊字符
    for target in PUNCTUATION['special_key']:  # 每一行逐个查找KEY是否存在
        finds = findTool.findAreaByStr(target, string)

        for position in finds:
            _color([rowIndex] + position, 'warning')

    # 自定义关键字
    for target in PUNCTUATION['key_word']:
        finds = findTool.findAreaByStr(target, string)

        for position in finds:
            _color([rowIndex] + position, 'key_word')

    # 括号
    for target in PUNCTUATION['special_range']:
        finds = findTool.findAreaBySignalPart(target[:2], string, target[2])

        for position in finds:
            _color([rowIndex] + position, 'bracket')

    # 引号
    for target in PUNCTUATION['say_signal']:
        finds = findTool.findAreaBySignalPart(target[:2], string, target[2])

        for position in finds:
            _color([rowIndex] + position, 'say')


# inline end ,say secondly,don't pay attention at foregoing codes


def initialize(**args):
    """
    核心editor初始化
    required arguments:
    MAIN_WINDOW UI_WIDGETS MAIN_CALL
    """
    global SELF_MC, SELF_MW, SELF_UI
    SELF_MW = args['MAIN_WINDOW']
    SELF_UI = args['UI_WIDGETS']
    SELF_MC = args['MAIN_CALL']

    setTags()


def setTags():
    """
    Config tags for color the word first.
    
    color meaning:
    key_word: key word,say: characters' say,bracket: bracket,
    warning: unexpected char
    """
    SELF_UI.textViewer.tag_config('say', foreground='green')
    SELF_UI.textViewer.tag_config('bracket', foreground='blue')
    SELF_UI.textViewer.tag_config('key_word', foreground='orange')
    SELF_UI.textViewer.tag_config('warning', foreground='red', background='yellow')


def check(**args):
    """Main function to call."""
    startTime = time.time()
    # Save the insert position
    insertRow, insertColumn = map(int, SELF_UI.textViewer.index('insert').split('.'))
    nowRowIndex = insertRow - 1

    content = SELF_UI.textViewer.get('1.0', 'end')
    rows = content.split('\n')[:-1]  # split the content row by row,needn't the last row(it is empty!!!)

    SELF_MC['log']('Scanning the file row by row...')

    _scanRow(nowRowIndex, rows[nowRowIndex])  # FIXME initialize can't scan all file

    SELF_UI.textViewer.mark_set('insert', f'{insertRow}.{insertColumn}')  # FIXME flash insert

    spentTime = round(time.time() - startTime, 2)
    SELF_MC['log'](f'Finished checking in {spentTime}s,insert position {insertRow}.{insertColumn}...')


# TODO 主程序类接口
class codeEditor(base.BaseExtension):
    pass
