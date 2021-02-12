Editor
===
# editor:
editor包括了编辑器，查找替换等功能，通过拓展的方式加载到主窗体上。  
editor下包含local配置文件（有无无关），可将editor源文件内字典创建为json对象，然后重新编辑即可  
PS：字典名叫做“标点”，但是用途不止这些  
```python
PUNCTUATION = {
    "special_key": ["a", "#", "小说", "·", "：", ":", "电子书"],
    "key_word": [],
    "special_range": [["'", "'", False], ["\"", "\"", False], ["[", "]", True]],
    "say_signal": [["“", "”", True], ["‘", "’", True]]
}
# I suggest you add special_range's signal to special_key,that you can know the wrong signals
# wrong signals can not be selected and colored,it well still high-light
```

# findTool:
findTool为代码编辑器提供了查找功能，使用类似于正则表达式的有限状态机进行查找。
findTool不仅用于查找替换，更复杂的关键字匹配，范围符号匹配也调用了FT。

## FindTool's interface:

```python
findAreaByStr(condition,string)->list:...
findAreaBySignalPart(condition,string)->list:...
# all return [[startIndex,length]]
```

# Extension Interface

## add_signal(kind,obj)
添加染色规则，具体见代码注释
## remove_signal(kind,obj)
和上面相反
## check(**arg)
立刻检查，参数见代码