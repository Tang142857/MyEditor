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
SPECIAL_CHARS = [r'\!', r'\@', r'\#', r'\$', r'\%', r'\^', r'\&', r'\*']  # 这里为了使用re就只能写成两个字符，一会要特殊计算偏移量
KEY_WORDS = ['main']


def setTags(text):
    """Config tags for color the word first."""
    text.tag_config('say', foreground='green')
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

    for index, row in enumerate(rows):  # here is rows list

        # 特殊字符
        for target in SPECIAL_CHARS:  # 每一行逐个查找KEY是否存在
            starts = [found.start() for found in re.finditer(target, row)]  # get chars index
            for start in starts:
                text.delete(f'{index+1}.{start}', f'{index+1}.{start+len(target)-1}')  # 注意，特殊字符偏移量不同
                text.insert(f'{index+1}.{start}', target.replace('\\', ''), 'warning')  # 注意，特殊字符去掉转义，give it back

        # 自定义关键字
        for target in KEY_WORDS:  # 每一行逐个查找KEY是否存在
            starts = [found.start() for found in re.finditer(target, row)]  # get chars index
            for start in starts:
                text.delete(f'{index+1}.{start}', f'{index+1}.{start+len(target)}')
                text.insert(f'{index+1}.{start}', target, 'key')

    text.mark_set('insert', f'{insertRow}.{insertColumn}')
    logEvent.emit(f'Finish checking, back insert{insertRow}.{insertColumn}...')
