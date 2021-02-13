扩展
===
# Extension
extension负责实现应用的其他功能  
MyEditor内置了部分插件来提供较为基础的功能，请不要尝试卸载内置插件，RUN_ONCE定义了启动加载的插件  

# Extension规则
//当前规则仅为临时使用，正式规则将随1.0版本确定  
extension的核心思想是：（每个）扩展只干一件事，其余交互来解决  

尽可能使用ME顶层目录进行导入（apply统一append to sys.path）  
一般来说使用getElement存取器拿到对象然后操作，不调用extension_interfaces  
扩展的接口类一般轻量级，不在类体内直接定义函数（维护起来也不方便）  

extension必须继承extensions.base.BaseExtension类，以确保正确重写了每一个需要的函数  
extension可以并建议在自身目录下生成local.json本地配置文件  
extension必须具有main模块，并保证含有Extension类，loader通过该类引导插件加载  
建议扩展事件采用Event类，参数列表为(self,event_args,other arg...)  
屏幕左侧的tool bar分配给了extension，可以往上面放置组件  