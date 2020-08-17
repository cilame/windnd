def _func(ls):
    for i in ls:
        print(i)


def hook_dropfiles(tkwindow_or_winfoid,func=_func,force_unicode=False):
    """
    # this func to deal drag icon & drop to load in windows
    *args:
        hwnd
    **kw:
        func = _func
        # default func just use path list print each one.
        # default each full_path_file_name type: bytes; in py3
        # default each full_path_file_name type: str  ; in py2
        #===================
        def _func(ls):
            for i in ls:
                print(i)
        #===================
    test evironment:
        py2, py3
        work on win7 32bit & 64bit.
    
    if you use tk, you can hook like this:
    =================================================
    > import windnd
    >
    > def my_func(ls):
          for idx,i in enumerate(ls):
              print(idx,i)
    >
    > import tkinter
    > tk = tkinter.Tk()
    > hwnd = tk.winfo_id()
    >
    > # you don't have to write "hwnd = tk.winfo_id()" in tkinter
    > # because you can put "tk" in this function like:
    > # "windnd.hook_dropfiles(tk,func = my_func)"
    > # the reason for this is to expand interface
    >
    > windnd.hook_dropfiles(hwnd,func = my_func)
    >
    > tk.mainloop()
    =================================================
    """
    
    # this place just for expand interface
    # because may anther window tools need use hwnd to hook
    # If you want to process .lnk , you can look at examples from the source code

    import platform
    import ctypes
    from ctypes.wintypes import DWORD

    hwnd = tkwindow_or_winfoid.winfo_id()\
           if getattr(tkwindow_or_winfoid, "winfo_id", None)\
           else tkwindow_or_winfoid

    if platform.architecture()[0] == "32bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongW
        SetWindowLong = ctypes.windll.user32.SetWindowLongW
        argtype = DWORD
    elif platform.architecture()[0] == "64bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongPtrA
        SetWindowLong = ctypes.windll.user32.SetWindowLongPtrA
        argtype = ctypes.c_uint64

    prototype = ctypes.WINFUNCTYPE(argtype,argtype,argtype,argtype,argtype)
    WM_DROPFILES = 0x233
    GWL_WNDPROC = -4
    create_buffer = ctypes.create_unicode_buffer if force_unicode else ctypes.c_buffer
    func_DragQueryFile = ctypes.windll.shell32.DragQueryFileW if force_unicode else ctypes.windll.shell32.DragQueryFile

    def py_drop_func(hwnd,msg,wp,lp):
        global files
        if msg == WM_DROPFILES:
            count = func_DragQueryFile(argtype(wp),-1,None,None)
            szFile = create_buffer(260)
            files = []
            for i in range(count):
                func_DragQueryFile(argtype(wp),i,szFile,ctypes.sizeof(szFile))
                dropname = szFile.value
                files.append(dropname)
            func(files)
            ctypes.windll.shell32.DragFinish(argtype(wp))
        return ctypes.windll.user32.CallWindowProcW(*map(argtype,(globals()[old],hwnd,msg,wp,lp)))

    # for limit hook number, protect computer.
    limit_num = 200
    for i in range(limit_num):
        if i+1 == limit_num:
            raise "over hook limit number 200, for protect computer."
        if "old_wndproc_%d" % i not in globals():
            old, new = "old_wndproc_%d"%i, "new_wndproc_%d"%i
            break

    globals()[old] = None
    globals()[new] = prototype(py_drop_func)

    ctypes.windll.shell32.DragAcceptFiles(hwnd,True)
    globals()[old] = GetWindowLong(hwnd,GWL_WNDPROC)
    SetWindowLong(hwnd,GWL_WNDPROC,globals()[new])


if __name__ == '__main__':
    def myfunc(ls):
        def _local_lnk(link):
            ''' 处理 link 指向的问题。'''
            import platform
            if platform.python_version().startswith('3') and type(link) is bytes:
                try:
                    _link = link.decode()
                except:
                    _link = link.decode('gbk')
            else:
                _link = link
            try:
                import sys, win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(_link)
                return shortcut.Targetpath if shortcut.Targetpath.strip() else _link
            except:
                return _link
        for i in ls:
            print('deal link:',_local_lnk(i))

    def test():
        '''
        将 windows 桌面的图标拖拽到被挂钩的窗口内
        对加载到的图标路径进行对应处理的函数。
        '''
        import tkinter
        tk = tkinter.Tk()
        hook_dropfiles(tk, myfunc)
        tk.mainloop()

    test()