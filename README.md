# windnd
windows drag icon and drop to load abs path.<br>
it can use pip install: <br>
<br>
```
C:\Users\Administrator>pip install windnd<br>
```
<br>
==============================================<br>
这是一个 windows 上使用的图表拖动加载地址的工具。<br>
为了在使用 tkinter 时候能更好的实现拖拽加载功能。<br>
测试代码：<br>
<br>
```
try:
    import tkinter<br>
except:
    import Tkinter as tkinter

import windnd
tk = tkinter.Tk()
windnd.hook_dropfiles(tk)
tk.mainloop()
```
==============================================<br>
hook_dropfiles函数有两个参数<br>
第一个：窗口信息，可以直接传 tkinter 的窗口，也可以传窗口 hwnd 的数字。<br>
第二个：执行函数，默认是一个收集所有拖进来的地址进行遍历打印输出的函数。<br>
<br>
默认函数：<br>
```
def _func(ls):
    for i in ls:
        print(i)
```
