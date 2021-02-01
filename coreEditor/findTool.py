"""
A model for editor to find something.Just like re{}

@author tang142857
introduction:
类似于正则表达式的查找模块，用于进行关键字染色（符号对支持，嵌套支持）和后期的查找功能
正则原理：基于状态机的正则引擎（不使用标准正则语句）
"""


def _getSide(condition, nextSide):
    """生成一条边，边的条件和下一条边要在这时确定"""
    def _side(string: str, index: int):
        """
        string: main string from match()
        index: now side's index
        next side: if condition is right ,will call the next side.
        """
        if string[index] == condition:
            return nextSide(string, index + 1)
        else:
            return None

    return _side


def _getEndSide(condition):
    """生成终边，其他与_getSide一致"""
    def _endSide(string: str, index: int):
        """
        almost the same as side(),but if my condition is right,well return myIndex.

        string: main string from match()
        index: now side's index
        No next side.
        """
        if string[index] == condition:
            return index
        else:
            return None

    return _endSide


if __name__ == '__main__':
    t = 'abcdefabcedfjkjdsakjdncxmn(cndjaskncj(ccxzc)cx)'
    f = _getSide('a', _getEndSide('b'))
    for index, ch in enumerate(t):
        if ch == 'a':
            r = f(t, index)
            print(r)
