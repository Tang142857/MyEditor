Editor
===
#### editor:
editor包括了代码编辑器，查找替换等功能，通过拓展的方式加载到主窗体上。

#### findTool:
findTool为代码编辑器提供了查找功能，使用类似于正则表达式的有限状态机进行查找。
findTool不仅用于查找替换，更复杂的关键字匹配，范围符号匹配也调用了FT。

##### FindTool's interface:

```python
findAreaByStr(condition,string)->list:...
findAreaBySignalPart(condition,string)->list:...
# all return [[startIndex,length]]
```