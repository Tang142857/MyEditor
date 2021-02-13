"""
code editor for MyEditor
@author: tang142857
Copyright(c) DFSA Software Develop Center

主编辑器函数，提供 关键字高亮，缩进增强，搜索字符串 等服务
在每次释放键盘<keyRelease>后都执行，尽可能小
后期支持自定义关键字

TBC extend standard
都保证包含了：initialize（初始化插件）
"""
import json
import time
import tkinter
from tqdm import tqdm

from Element import mainEvent, dialog
from extensions import base
from extensions.core_editor import findTool

PUNCTUATION = {
    "special_key": ["a", "#", "小说", "·", "：", ":", "电子书"],
    "key_word": [],
    "special_range": [["'", "'", False], ["\"", "\"", False], ["[", "]", True]],
    "say_signal": [["“", "”", True], ["‘", "’", True]]
}

try:
    with open('\\'.join(__file__.split('\\')[:-1]) + '\\local.json', 'r', encoding='utf-8') as config:
        localConfig = json.loads(config.read())
except FileNotFoundError as msg:
    print(f'Config not found at editor {msg},I am at {__file__}')
else:
    PUNCTUATION.update(localConfig)

# ui args start,all name with SELF_... ，用户UI，发射事件的时候是只有event的，提前储存“指针”
SELF_MW = None
SELF_UI = None
update_status = None
console_log = None


def _color(positionList: list, kind: str):
    """
    color the string with marks.\n
    required arguments:positionList[row,startindex,length],kind: mark name
    attention: all argments use index(start at 0)!!!
    """
    row_index = positionList[0]
    start_index = positionList[1]
    length = positionList[2]
    # get arguments

    _str = SELF_UI.textViewer.get(f'{row_index + 1}.{start_index}', f'{row_index + 1}.{start_index + length}')
    # get text before deleting it,for insert it again
    SELF_UI.textViewer.delete(f'{row_index + 1}.{start_index}', f'{row_index + 1}.{start_index + length}')
    # delete the string in text before
    SELF_UI.textViewer.insert(f'{row_index + 1}.{start_index}', _str, kind)


def _scanRow(rowIndex: int, string: str):
    """
    Scan the row and color words.Use public interface needn't other arguments.
    """
    # update the row first to clean the outdate marks off
    SELF_UI.textViewer.delete(f'{rowIndex + 1}.0', f'{rowIndex + 1}.{len(string)}')
    SELF_UI.textViewer.insert(f'{rowIndex + 1}.0', string)

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


def _setTags():
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


def _check(*arg, **args):
    """check content (not noly for code,but also for novel or .lrc and so on)."""
    arguments = {'init': False}
    arguments.update(args)
    startTime = time.time()

    # Save the insert position
    insertRow, insertColumn = map(int, SELF_UI.textViewer.index('insert').split('.'))
    nowRowIndex = insertRow - 1

    content = SELF_UI.textViewer.get('1.0', 'end')
    rows = content.split('\n')[:-1]  # split the content row by row,needn't the last row(it is empty!!!)

    if arguments['init']:
        for index, strRow in enumerate(tqdm(rows, ncols=80, desc='Scanning:')):
            _scanRow(index, strRow)
    else:
        _scanRow(nowRowIndex, rows[nowRowIndex])

    SELF_UI.textViewer.mark_set('insert', f'{insertRow}.{insertColumn}')  # give the insert back

    if arguments['init']: update_status(f'Checking finished in {round(time.time() - startTime, 2)}s.')


class EditMenu(tkinter.Menu):
    """Editor menu bar"""
    def __init__(self, master):
        """Master=mainWindowMenu"""
        super().__init__(master, tearoff=False)
        # initialize father widget
        self.conutPress = mainEvent.BaseEvent()
        self.checkAllPreaa = mainEvent.BaseEvent()
        self.addRulePress = mainEvent.BaseEvent()
        self.removeRulePress = mainEvent.BaseEvent()
        # create signal

        self.add_command(label='Conut', command=self.conutPress.emit)
        self.add_command(label='Recheck All', command=self.checkAllPreaa.emit)
        self.add_command(label='Add rule', command=self.addRulePress.emit)
        self.add_command(label='Remove rule', command=self.removeRulePress.emit)


class CodeEditor(base.BaseExtension):
    """基本都是直接调用了，直接看函数注释"""
    def __init__(self, interface):
        super().__init__(interface)

    def on_load(self, **arg):
        """
        On load function of core editor

        addition: menu bar,event bind,tags of text viewer(remove these thing when unload)
        """
        global SELF_UI, SELF_MW, update_status
        SELF_MW = self._get_element('MAIN_WINDOW')
        SELF_UI = self._get_element('UI_WIDGETS')
        update_status = self._get_element('log')
        self._menuBar = EditMenu(SELF_MW)
        # set self global variables end

        self._get_element('MAIN_WINDOW>bind')('<KeyRelease>', _check)
        self._get_element('UI_WIDGETS>textViewer').event_add("<<set-line-and-column>>", "<KeyRelease>",
                                                             "<ButtonRelease>")
        self._get_element('UI_WIDGETS>textViewer').bind('<<set-line-and-column>>', self._update_line_and_column)
        self._get_element('UI_WIDGETS>mainWindowMenu').add_cascade(label='Editor', menu=self._menuBar)
        self.position_show_label = tkinter.Label(self._get_element('UI_WIDGETS>statusShowFrame'),
                                                 background='#007ACC',
                                                 text='Row:0,Col:0',
                                                 font=('Microsoft YaHei', 9))
        self.position_show_label.pack(side='right')
        # config main window

        _setTags()
        _check(init=True)
        # initialize run

        self._menuBar.checkAllPreaa.add_callback(self._checkAll)
        self._menuBar.addRulePress.add_callback(self._add_signal)

        self._get_element('log')('load core editor end')

    def un_load(self):
        self._get_element('log')('unloading core editor...')

    def _update_line_and_column(self, event=None):
        r_position, c_position = self._get_element('UI_WIDGETS>textViewer').index('insert').split('.')
        self.position_show_label.config(text=f'Row:{r_position},Col:{c_position}')

    def _checkAll(self):
        _check(init=True)

    def _add_signal(self):
        name = dialog.ask('Add rule', 'Enter new rule.')
        if name is None: return
        self.add_signal('special_key', name)

    def check(self, *arg, **args):
        _check(*arg, **args)

    def add_signal(self, kind: str, obj):
        """Add signal."""
        try:
            PUNCTUATION[kind].append(obj)
            return None
        except Exception as msg:
            return msg

    def remove_signal(self, kind: str, obj):
        """Remove signal"""
        try:
            PUNCTUATION[kind].remove(obj)
            return None
        except Exception as msg:
            return msg
