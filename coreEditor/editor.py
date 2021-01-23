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


def check(text):
    """Main function to call."""
    logEvent.emit('Checking...')
    content = text.get(1.0, 'end')
