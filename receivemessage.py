import sys
import win32gui
import win32api
import ctypes
from ctypes import wintypes
from datetime import datetime

def main():
    if len(sys.argv) == 1:
        message = input("enter message: ")
    else:
        message = sys.argv[1]

    if message == "":
        exit

    messageId = win32api.RegisterWindowMessage(message)
    
    if messageId == 0:
        print("RegisterWindowMessage fail")

        exit

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    LRESULT = ctypes.c_longlong
    
    HCURSOR = wintypes.HANDLE
    
    WNDPROC = ctypes.WINFUNCTYPE(
        LRESULT,
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM
    )
    
    class WNDCLASS(ctypes.Structure):
        _fields_ = [
            ('style', wintypes.UINT),
            ('lpfnWndProc', WNDPROC),
            ('cbClsExtra', ctypes.c_int),
            ('cbWndExtra', ctypes.c_int),
            ('hInstance', wintypes.HINSTANCE),
            ('hIcon', wintypes.HICON),
            ('hCursor', HCURSOR),
            ('hbrBackground', wintypes.HBRUSH),
            ('lpszMenuName', wintypes.LPCWSTR),
            ('lpszClassName', wintypes.LPCWSTR),
        ]

    @WNDPROC
    def window_proc(hwnd, msg, wparam, lparam):
        if msg == messageId:
            print(f'{datetime.now()} Получено сообщение {message} ({msg}): {wparam}, {lparam}')
            
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    wc = WNDCLASS()
    wc.style = 0
    wc.lpfnWndProc = window_proc
    wc.cbClsExtra = 0
    wc.cbWndExtra = 0
    wc.hInstance = kernel32.GetModuleHandleW(None)
    wc.hIcon = None
    wc.hCursor = None
    wc.hbrBackground = None
    wc.lpszMenuName = None
    wc.lpszClassName = 'MyWindowClass'

    atom = user32.RegisterClassW(wc)
    
    if not atom:
        raise Exception("Ошибка регистрации класса окна")

    hwnd = win32gui.CreateWindow(
        wc.lpszClassName,
        'Тестовое окно',
        0,
        0, 0, 800, 600,
        None,
        None,
        wc.hInstance,
        None
    )

    if not hwnd:
        raise Exception("Ошибка создания окна")
    
    while True:
        msg = wintypes.MSG()
        
        if user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        else:
            break

if __name__ == "__main__":
    main()