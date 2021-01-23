"""
main editor function
@author: tang142857
Copyright(c) DFSA Software Develop Center

主编辑器函数，提供 关键字高亮，缩进增强，搜索字符串等服务
在每次释放键盘<key-release>后都执行，尽可能小
后期支持自定义关键字
"""
from coreElement.mainEvent import EditorLogEvent

logEvent = EditorLogEvent()
KEY_CHAR = ['!', '@', '#', '$', '%', '^', '&', '*']


def setTags(text):
    """Config tags for color the word first."""
    text.tag_config('say', foreground='green')
    text.tag_config('warning', foreground='red', background='yellow')


def check(text, event):
    """Main function to call."""
    logEvent.emit(f'Checking {event.__str__()}...')

    content = text.get('0.0', 'end')
    text.delete('0.0', 'end')  # clean up the space
    for char in content[:-1]:  # needn't the last \n
        if char in KEY_CHAR:
            text.insert('insert', char, 'warning')  # 特殊符号警告
        else:
            text.insert('insert', char)  # FIXME wrong insert position

    logEvent.emit('Finish checking...')
