"""
A model for editor to find something.Just like re{}

@author tang142857

introduction:
类似于正则表达式的查找模块，用于进行关键字染色（符号对支持，嵌套支持）和后期的查找功能
正则原理：基于状态机的正则引擎（不使用标准正则语句）
"""


# side creator define start here
def _getSide(condition, nextSide):
    """生成一条边，边的条件和下一条边要在这时确定"""
    def _side(string: str, index: int):
        """
        有向图中的单边\n
        string: main string from match()
        index: now side's index
        next side: if condition is right ,will call the next side.
        """
        if string[index] == condition:
            return nextSide(string, index + 1)
        else:
            return None

    def _interSide(string: str, index: int):
        """
        有向图中的多边，即同时连接了两条边\n
        string: main string from match()
        index: now side's index
        next side: if condition is right ,will call the next side.
        """

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
        if string[index] == condition:  # FIXME out of index error,if first condition at the line end
            return index
        else:
            return None

    return _endSide


# side creator end here


def _splitCondition(condition: str):
    """Split the str condition to condition,just like \d \n..."""
    if condition == '':
        raise Exception('Please input your condition except empty!!!')

    newCondition = []
    for i in range(len(condition)):  # 颠倒条件
        newCondition.append(condition[-(i + 1)])

    return newCondition  # not support standard re expression until 2.0


def _createAutoMachine(condition: str):
    """生成自动机用于find函数启动匹配，注意自动机是根据表达式从后往前生成"""
    conditions = _splitCondition(condition)
    # get splited,upside down condition
    lastSide = _getEndSide(conditions[0])
    # create end side before create other sides
    for condition in conditions[1:]:
        lastSide = _getSide(condition, lastSide)

    return lastSide, conditions[-1]


# Public function start


def findAreaByStr(condition: str, string: str):
    """
    Find area by string(not support re expression until 2.0)\n
    :return: [[startIndex,length]]
    """
    machine, firstCondition = _createAutoMachine(condition)
    outputArea = []

    for index, ch in enumerate(string):
        if ch == firstCondition:  # 字符串匹配到第一条件，启动状态机
            startIndex = index  # remember start index
            endIndex = machine(string, index)
            if endIndex is not None:
                outputArea.append([startIndex, endIndex - startIndex + 1])
                # return length with the first char ,so add 1

    return outputArea


if __name__ == '__main__':
    t = 'abcdefabcedfjkjdsakjdncxmn(cndjaskncj(ccxzc)cx)'
    print(findAreaByStr('abc', t))
