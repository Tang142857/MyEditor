"""
A model for editor to find something.Just like re{}

@author tang142857
introduction:
类似于正则表达式的查找模块，用于进行关键字染色（符号对支持，嵌套支持）和后期的查找功能
正则原理：基于状态机的正则引擎（不使用标准正则语句）
"""


def _getSide(target, nextSide):
    """生成一条边，边的条件和下一条边要在这时确定"""
    def _side(string: str, index: int):
        """
        You must pay attention that if the side is the begin side,index should -1 (I will add 1).\n

        string: main string from match()
        index: the last side's index
        next side: if condition is right ,will call the next side.
        """
        myIndex = index + 1
        if string[myIndex] == target:
            return nextSide(string, myIndex)
        else:
            return None

    return side


def _getEndSide(target):
    """生成终边，其他与_getSide一致"""
    def _endSide(string: str, index: int):
        """
        almost the same as side(),but if my condition is right,well return myIndex.

        string: main string from match()
        index: the last side's index
        No next side.
        """
        myIndex = index + 1
        if string[myIndex] == target:
            return myIndex
        else:
            return None