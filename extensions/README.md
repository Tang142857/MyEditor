扩展
===
# extension
extension负责实现应用的其他功能  
MyEditor内置了部分插件来提供较为基础的功能，请不要尝试卸载内置插件  

# extension规则
//当前规则仅为临时使用，正式规则将随1.0版本确定  
尽可能使用ME顶层目录进行导入（apply统一append to sys.path）

extension必须继承extensions.base.BaseExtension类，以确保正确重写了每一个需要的函数  
extension可以并建议在自身目录下生成local.json本地配置文件  
extension必须具有main模块，并保证含有Extension类，loader通过该类引导插件加载  