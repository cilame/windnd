def _func(ls):
    for i in ls:
        print(i)

def hook_dropfiles(hwnd,func=_func):
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
        python3.6
        work on win7 32bit & 64bit.
    
    if you use tk, you can hook like this:
    =================================================
    > import windnd
    >
    > def my_func(ls):
          for idx,i in enumerate(ls):
              print(idx,i)
    >
    > import tk
    > tk = tk.Tk()
    > hwnd = tk.winfo_id()
    >
    > windnd.hook_dropfiles(hwnd,func = my_func)
    >
    > tk.mainloop()
    =================================================
    """
    import platform
    import ctypes
    from ctypes.wintypes import DWORD
    prototype = ctypes.WINFUNCTYPE(DWORD,DWORD,DWORD,DWORD,DWORD)
    WM_DROPFILES = 0x233
    GWL_WNDPROC = -4

    def py_drop_func(hwnd,msg,wp,lp):
        global files
        if msg == WM_DROPFILES:
            count = ctypes.windll.shell32.DragQueryFile(wp,-1,None,None)
            szFile = ctypes.c_buffer(260)
            files = []
            for i in range(count):
                ctypes.windll.shell32.DragQueryFile(wp,i,szFile,ctypes.sizeof(szFile))
                dropname = szFile.value
                files.append(dropname)
            func(files)
            ctypes.windll.shell32.DragFinish(wp)
        return ctypes.windll.user32.CallWindowProcW(globals()[old],hwnd,msg,wp,lp)

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

    if platform.architecture()[0] == "32bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongW
        SetWindowLong = ctypes.windll.user32.SetWindowLongW
    elif platform.architecture()[0] == "64bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongPtrW
        SetWindowLong = ctypes.windll.user32.SetWindowLongPtrW

    ctypes.windll.shell32.DragAcceptFiles(hwnd,True)
    globals()[old] = GetWindowLong(hwnd,GWL_WNDPROC)
    SetWindowLong(hwnd,GWL_WNDPROC,globals()[new])

def text_on_tkinter():
    import tkinter
    t = tk.Tk()
    a = tk.Entry(t)
    b = tk.Entry(t)
    hook_dropfiles(a.winfo_id())
    hook_dropfiles(b.winfo_id())
    a.pack(side="top")
    b.pack(side="top")
    t.mainloop()

    
