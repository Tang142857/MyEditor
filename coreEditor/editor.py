"""
main editor function
@author: tang142857
Copyright(c) DFSA Software Develop Center

主编辑器函数，提供 关键字高亮，缩进增强，搜索字符串等服务
在每次释放键盘<key-release>后都执行，尽可能小
后期支持自定义关键字

TBC extend standard
都保证包含了：initialize（初始化插件）
"""
import re
import time
from coreEditor import findTool

# global variable define start
# SPECIAL_CHARS = [r'\!', r'\@', r'\#', r'\$', r'\%', r'\^', r'\&', r'\*', r'\d']  # 这里为了使用re就只能写成两个字符，一会要特殊计算偏移量
KEY_WORDS = ['main', 'if', '小说', '·', '：', ':', '电子书']
SPECIAL_RANGE = [("'", "'", True), ('"', '"', True), ("(", ")", False)]
SAY_SIGNAL = [("“", "”", True), ('‘', '’', True)]
SPECIAL_CHARS = ['a', '#']

# signals end

# ui args start,all name with SELF_... ，用户UI，发射事件的时候是只有event的，提前储存“指针”
SELF_MW = None
SELF_UI = None
SELF_MC = {}  # 核心调用 e.g. openFile


# inline start ,you needn't pay attention to here :)
class stack(object):
    def __init__(self):
        self.mainList = []  # a list to save Python object

    def put(self, obj):
        self.mainList.append(obj)

    def get(self):
        lastDate = self.mainList[-1]
        del self.mainList[-1]
        return lastDate

    def isEmpty(self):
        if self.mainList == []:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.mainList != []:
            return self.get()
        else:
            raise StopIteration


def startSymbol(start):
    """闭包，用于__findArea"""
    def endSymbol(end, full: bool):
        return [start, end, full]

    return endSymbol


def __findAreaByChar(char: str, string: str):
    """
    Find area by char.\nRequired arguments:char,string
    return [[startIndex,length]]
    """
    finds = []

    for index, ch in enumerate(string):
        if ch == char:
            finds.append([index, 1])

    return finds


def __findAreaByRe(reExpression, string):
    """
    Find area by re pattern.\nRequired argments:re expression,string
    return [[startIndex,length]]
    """
    pass  # TODO __findAreaByRe


def __findAreaByPart(part, string):
    """
    Find area by signal like ['(',')'].\nRequired argments:part,string
    return [[startIndex,length]]
    """
    pass  # TODO __findAreaByPart


def __findArea(string: str, start="(", end=")", near=True):
    """
    在字符串中匹配start和end包围起来的内容（括号，人物对话之类的）\n
    near:是否需要最近匹配，例如字符串引号就是最近，括号则是最远
    full:判断是否完整，bracket模式下不解析
    ouput:[start index,end index,full]

    这东西的逻辑复杂，首先，正常情况下应该先出现start，然后end，start
    时创建闭包保存index，到了end时，就取出最近的
    start并调用生成output。不正常的很好判断，直接从头到尾就行了
    """
    indexStack = stack()  # cell [start index,end index]
    indexList = []

    for index, char in enumerate(string):
        if char == start and (indexStack.isEmpty() or (not near)):
            indexStack.put(startSymbol(index))
        elif char == end:
            if indexStack.isEmpty():  # 空的说明没有前符号
                indexList.append([0, index, False])
            else:  # 正常，取出最近start
                indexList.append((indexStack.get())(index, True))
        else:
            pass

    for remain in indexStack:
        indexList.append(remain(index, False))

    return indexList


def __color(positionList: list, kind: str):
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
    SELF_UI.textViewer.tag_config('bracket', foreground='blue', background='red')
    SELF_UI.textViewer.tag_config('key_word', foreground='orange')
    SELF_UI.textViewer.tag_config('warning', foreground='red', background='yellow')


def check(**args):
    """Main function to call."""
    # SELF_MC['log'](f'Checking {event.__str__()}...')
    startTime = time.time()
    # Save the insert position
    insertRow, insertColumn = map(int, SELF_UI.textViewer.index('insert').split('.'))

    content = SELF_UI.textViewer.get('1.0', 'end')
    rows = content.split('\n')[:-1]  # split the content row by row,needn't the last row(it is empty!!!)

    SELF_MC['log']('Scanning the file row by row...')

    for rowIndex, strRow in enumerate(rows):  # TODO improve the speed of checking
        # update the row first to clean the outdate marks off
        SELF_UI.textViewer.delete(f'{rowIndex+1}.0', f'{rowIndex+1}.{len(strRow)}')
        SELF_UI.textViewer.insert(f'{rowIndex+1}.0', strRow)

        # 特殊字符
        for targetChar in SPECIAL_CHARS:  # 每一行逐个查找KEY是否存在
            finds = __findAreaByChar(targetChar, strRow)

            for position in finds:
                __color([rowIndex] + position, 'warning')

        # 自定义关键字
        for target in KEY_WORDS:  # 每一行逐个查找KEY是否存在
            starts = [found.start() for found in re.finditer(target, strRow)]  # get chars index

            for start in starts:
                SELF_UI.textViewer.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{start+len(target)}')
                SELF_UI.textViewer.insert(f'{rowIndex+1}.{start}', target, 'key_word')

        # 括号
        for targetMark in SPECIAL_RANGE:
            for area in __findArea(strRow, targetMark[0], targetMark[1], targetMark[2]):
                start, end = area[0], area[1]
                target = SELF_UI.textViewer.get(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                SELF_UI.textViewer.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                SELF_UI.textViewer.insert(f'{rowIndex+1}.{start}', target, 'bracket')

        # 引号
        for targetMark in SAY_SIGNAL:
            for area in __findArea(strRow, targetMark[0], targetMark[1], targetMark[2]):
                if area[2]:  # 正常
                    start, end = area[0], area[1]
                    target = SELF_UI.textViewer.get(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                    SELF_UI.textViewer.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                    SELF_UI.textViewer.insert(f'{rowIndex+1}.{start}', target, 'say')
                else:
                    start, end = area[0], area[1]
                    target = SELF_UI.textViewer.get(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                    SELF_UI.textViewer.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                    SELF_UI.textViewer.insert(f'{rowIndex+1}.{start}', target, 'bracket')

    SELF_UI.textViewer.mark_set('insert', f'{insertRow}.{insertColumn}')  # FIXME flash insert

    spentTime = round(time.time() - startTime, 2)
    SELF_MC['log'](f'Finished checking in {spentTime}s,insert position {insertRow}.{insertColumn}...')
