"""
A model for editor to find something.Just like re{}

@author tang142857

introduction:
类似于正则表达式的查找模块，用于进行关键字染色（符号对支持，嵌套支持）和后期的查找功能
"""


# side creator define start here
def _getSide(condition, nextSide):
    """生成普通一条边，边的条件和下一条边要在这时确定"""
    def _side(string: str, index: int):
        """
        有向图中的单边\n
        string: main string from match()
        index: now side's index
        next side: if condition is right ,will call the next side.
        """
        try:
            if string[index] == condition:
                return nextSide(string, index + 1)
            else:
                return None

        except IndexError:
            return None

    return _side


def _getRecyclableSide(nextSide):
    """生成二向边，边的条件和下一条边要在这时确定，condition使用endside的condition"""
    def _side(string: str, index):
        """
        特殊的边，支持多次匹配，condition即为结束条件\n
        not support self-define condition between range until 2.0
        """
        try:
            if (result := nextSide(string, index)):  # ask the next side ,is ok?(needn't add 1,if *)
                return result  # if next side is ok,return result
            elif string[index]:  # can't match the remaining machine,next character
                return _side(string, index + 1)

        except IndexError:
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
        try:
            if string[index] == condition:
                return index
            else:
                return None

        except IndexError:
            return None

    return _endSide


# side creator end here


def _splitCondition(condition: str):
    """Split the str condition to condition,just like \d \n..."""
    if condition == '': raise RuntimeError('Please input your condition except empty!!!')

    newCondition = []
    for i in range(len(condition)):  # 颠倒条件
        newCondition.append(condition[-(i + 1)])

    return newCondition  # not support standard re expression until 2.0


def _createAutoMachineByStr(condition: str):
    """生成自动机用于find函数启动匹配，注意自动机是根据表达式从后往前生成"""
    conditions = _splitCondition(condition)
    # get splited,upside down condition
    lastSide = _getEndSide(conditions[0])
    # create end side before create other sides
    for condition in conditions[1:]:
        lastSide = _getSide(condition, lastSide)

    return lastSide, conditions[-1]


def _createAutoMachineByList(condition: list, strict: bool):
    """符号对自动机生成器"""
    if len(condition) != 2: raise RuntimeError('Condition can be compiled.')

    # 严格匹配用该函数
    def _findNextBracket(string: str, nowBracketIndex: int):
        """
        Find the next/last bracket(I try my best to use re expression,but I failed :( )
        condition is the signal part list like ['(',')']

        :return: next/last bracket index
        """
        if (nowBracketIndex) >= len(string): return None
        # it is the last char of the string
        nowBracketIndex += 1
        layerNumberEntered = 0

        for index, char in enumerate(string[nowBracketIndex:]):
            index += nowBracketIndex  # get the real index
            if char == condition[0]:
                layerNumberEntered += 1  # enter one layer of bracket
            elif char == condition[1]:
                if not layerNumberEntered: return index
                else: layerNumberEntered -= 1  # jump out

        return None  # can't find the other part of signal

    # 宽松匹配用lastside
    lastSide = _getEndSide(condition[1])
    lastSide = _getRecyclableSide(lastSide)
    lastSide = _getSide(condition[0], lastSide)

    if strict: return _findNextBracket, condition[0]  # remember return start condition
    else: return lastSide, condition[0]


# Public function start


def findAreaByStr(condition: str, string: str):
    """
    Find area by string(not support re expression until 2.0)\n
    :return: [[startIndex,length]]
    """
    machine, firstCondition = _createAutoMachineByStr(condition)
    outputArea = []

    for index, ch in enumerate(string):
        if ch == firstCondition:  # 字符串匹配到第一条件，启动状态机
            startIndex = index  # remember start index
            endIndex = machine(string, index)
            if endIndex is not None:
                outputArea.append([startIndex, endIndex - startIndex + 1])
                # return length with the first char ,so add 1

    return outputArea


def findAreaBySignalPart(condition: list, string: str, isStrict=True):
    """
    Find area by 范围符号 like :() \n
    do not use limit ,it is just for inline function to use

    :return: [[startIndex,length]]
    """
    machine, firstCondition = _createAutoMachineByList(condition, isStrict)
    outputArea = []
    hadNotMatched = True

    for index, ch in enumerate(string):
        if (ch == firstCondition) and hadNotMatched:
            startIndex = index
            endIndex = machine(string, index)
            if endIndex is not None:
                outputArea.append([startIndex, endIndex - startIndex + 1])
                if not isStrict: hadNotMatched = not hadNotMatched

    return outputArea


if __name__ == '__main__':
    t = 'mn"dsdhdh"abcsajkdh"a)'
    print(findAreaByStr('abc', t))
    print(findAreaBySignalPart(['"', '"'], t, False))
