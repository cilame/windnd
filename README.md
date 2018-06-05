# windnd
windows drag icon and drop to load abs path.

it can use pip install: 
C:\Users\Administrator>pip install windnd

==============================================
这是一个 windows 上使用的图表拖动加载地址的工具。
为了在使用 tkinter 时候能更好的实现拖拽加载功能。

测试代码：

try:
    import tkinter
except:
    import Tkinter as tkinter

import windnd
tk = tkinter.Tk()
windnd.hook_dropfiles(tk)
tk.mainloop()

==============================================
hook_dropfiles函数有两个参数
第一个：窗口信息，可以直接传 tkinter 的窗口，也可以传窗口 hwnd 的数字。
第二个：执行函数，默认是一个收集所有拖进来的地址进行遍历打印输出的函数。

默认函数：
def _func(ls):
    for i in ls:
        print(i)
