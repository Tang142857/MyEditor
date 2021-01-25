"""
main editor function
@author: tang142857
Copyright(c) DFSA Software Develop Center

主编辑器函数，提供 关键字高亮，缩进增强，搜索字符串等服务
在每次释放键盘<key-release>后都执行，尽可能小
后期支持自定义关键字
"""
import re

from coreElement.mainEvent import EditorLogEvent

logEvent = EditorLogEvent()
SPECIAL_CHARS = [r'\!', r'\@', r'\#', r'\$', r'\%', r'\^', r'\&', r'\*', r'\d']  # 这里为了使用re就只能写成两个字符，一会要特殊计算偏移量
KEY_WORDS = ['main', 'if', '小说', '·', '：', ':']
SPECIAL_RANGE = [("'", "'", True), ('"', '"', True), ("“", "”", True), ("(", ")", False), ('‘', '’', True)]


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
    def endSymbol(end):
        return [start, end]

    return endSymbol


def __findArea(string: str, start="(", end=")", near=True):
    """
    在字符串中匹配start和end包围起来的内容（括号，人物对话之类的）\n
    near:是否需要最近匹配，例如字符串引号就是最近，括号则是最远
    ouput:[start index,end index]

    这东西的逻辑复杂，首先，正常情况下应该先出现start，然后end，start
    时创建修饰器保存index，到了end时，就取出最近的
    start并调用生成output。不正常的很好判断，直接从头到尾就行了
    """
    indexStack = stack()  # cell [start index,end index]
    indexList = []

    for index, char in enumerate(string):
        if char == start and (indexStack.isEmpty() or (not near)):
            indexStack.put(startSymbol(index))
        elif char == end:
            if indexStack.isEmpty():  # 空的说明没有前符号
                indexList.append([0, index])
            else:  # 正常，取出最近start
                indexList.append((indexStack.get())(index))
        else:
            pass

    for remain in indexStack:
        indexList.append(remain(index))

    return indexList


# inline end


def setTags(text):
    """Config tags for color the word first."""
    text.tag_config('say', foreground='green')
    text.tag_config('bracket', foreground='blue', background='red')
    text.tag_config('key', foreground='orange', underline=True)
    text.tag_config('warning', foreground='red', background='yellow')


def check(text, event):
    """Main function to call."""
    logEvent.emit(f'Checking {event.__str__()}...')
    # Save the insert position
    insertRow, insertColumn = map(int, text.index('insert').split('.'))

    content = text.get('1.0', 'end')
    rows = content.split('\n')[:-1]  # split the content row by row,needn't the last row(it is empty!!!)

    logEvent.emit('Scanning the file row by row...')

    for rowIndex, strRow in enumerate(rows):  # here is rows list
        # update the row first to clean the outdate marks off
        text.delete(f'{rowIndex+1}.0', f'{rowIndex+1}.{len(strRow)}')
        text.insert(f'{rowIndex+1}.0', strRow)

        # 特殊字符
        for target in SPECIAL_CHARS:  # 每一行逐个查找KEY是否存在
            finder = re.compile(target)
            starts = [found.start() for found in finder.finditer(strRow)]
            matches = [found.group() for found in finder.finditer(strRow)]

            for colIndex, start in enumerate(starts):
                text.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{start+len(target)-1}')  # 注意，特殊字符偏移量不同
                text.insert(f'{rowIndex+1}.{start}', matches[colIndex], 'warning')  # 注意，特殊字符去掉转义，give it back

        # 自定义关键字
        for target in KEY_WORDS:  # 每一行逐个查找KEY是否存在
            starts = [found.start() for found in re.finditer(target, strRow)]  # get chars index

            for start in starts:
                text.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{start+len(target)}')
                text.insert(f'{rowIndex+1}.{start}', target, 'key')

        # 括号
        for targetMark in SPECIAL_RANGE:
            for area in __findArea(strRow, targetMark[0], targetMark[1], targetMark[2]):
                start, end = area[0], area[1]
                target = text.get(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                text.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                text.insert(f'{rowIndex+1}.{start}', target, 'bracket')

    text.mark_set('insert', f'{insertRow}.{insertColumn}')  # FIXME wrong position at row end
    logEvent.emit(f'Finish checking ,insert position {insertRow}.{insertColumn}...')
