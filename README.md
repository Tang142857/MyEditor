Text Book Checker
===
#### 说明

简易可扩展编辑器

#### Setup

克隆本仓库到本地  
```bash
git clone https://github.com/Tang142857/TextbookChecker.git
```
执行入口apply.py  

#### 程序

##### 文件

textbookchecker  
│  .gitignore  
│  apply.py--(主程序入口)  
|  exceptions.py--(异常类)  
│  LICENSE  
│  README.md  
│  
├─coreEditor--(编辑器模块)  
│  │  editor.py  
│  │  __init__.py  
│  
├─Element--(核心元素模块)  
│  │  book.py  
│  │  mainEvent.py--(主要事件)  
│  │  ui.py--(用户界面)  
│  │  __init__.py  

##### 框架
apply作为主程序，管理核心事件，负责加载所有的模块  
UI内部提供交互事件关联到apply中的处理函数，作为单独的模块被加载  
主要事件存放在mainEvent，被各个模块加载，因为都基于BaseEvent  
编辑器提供检查服务  

extend通过初始化传入的参数运行，包括了用户界面和核心调用（文件存取）  
```python
extendInitArgs = {
    'MAIN_WINDOW': MAIN_WINDOW,
    'UI_WIDGETS': UI_WIDGETS,
    'MAIN_CALL': {
        'log': log,
        'copy_content': copyContent,
        'open_file': openFile,
        'open_work_dir': openWorkDir,
        'save': save,
        'close_file': closeFile
    }
}
```
apply除了启动，调用extend，加载、关闭文件，维持用户界面外什么都不干  