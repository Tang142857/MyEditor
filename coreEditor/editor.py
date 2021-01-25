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
SPECIAL_RANGE = [("'", "'"), ('"', '"'), ("“", "”"), ("(", ")"), ('‘', '’')]


def setTags(text):
    """Config tags for color the word first."""
    text.tag_config('say', foreground='green')
    text.tag_config('bracket', foreground='blue', background='red')
    text.tag_config('key', foreground='orange', underline=True)
    text.tag_config('warning', foreground='red', background='yellow')


def __findArea(string: str, start='“', end='”'):  # FIXME 多重括号！！！
    """在字符串中匹配start和end包围起来的内容（括号，人物对话之类的）"""
    indexList = []  # cell [start index,end index]
    inRange = False
    cell = [0, 0]

    for index, char in enumerate(string):
        if char == start and (not inRange):  # enter range
            inRange = True
            cell[0] = index
        elif char == end:
            if inRange:  # 只有前符号的（多半有问题）
                cell[1] = index
                indexList.append(cell)
                cell = [0, 0]
                inRange = False
            else:
                cell[0], cell[1] = 0, index
                indexList.append(cell)
                cell = [0, 0]
                inRange = False
        else:
            pass

    if inRange:  # 超出去了
        cell[1] = len(string) - 1
        indexList.append(cell)

    return indexList


def check(text, event):
    """Main function to call."""
    logEvent.emit(f'Checking {event.__str__()}...')
    # Save the insert position
    insertRow, insertColumn = map(int, text.index('insert').split('.'))

    content = text.get('1.0', 'end')
    rows = content.split('\n')[:-1]  # split the content row by row,needn't the last row(it is empty!!!)

    logEvent.emit('Scanning the file row by row...')

    for rowIndex, strRow in enumerate(rows):  # here is rows list

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
        for targetMark in SPECIAL_RANGE:  # FIXME 无法归还修正的mark
            for area in __findArea(strRow, targetMark[0], targetMark[1]):
                start, end = area[0], area[1]
                target = text.get(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                text.delete(f'{rowIndex+1}.{start}', f'{rowIndex+1}.{end+1}')
                text.insert(f'{rowIndex+1}.{start}', target, 'bracket')

    text.mark_set('insert', f'{insertRow}.{insertColumn}')  # 鼠标放回去
    logEvent.emit(f'Finish checking ,insert position {insertRow}.{insertColumn}...')
