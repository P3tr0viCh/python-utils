import sys
import win32api
import win32con

def main():
    if len(sys.argv) == 1:
        message = input("enter message: ")
    else:
        message = sys.argv[1]

    if message == "":
        exit
        
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        wParam = int(sys.argv[2])
    else:
        wParam = 0

    messageId = win32api.RegisterWindowMessage(message)

    if messageId == 0:
        print("RegisterWindowMessage fail")

        exit

    print("RegisterWindowMessage ok")
    
    win32api.PostMessage(win32con.HWND_BROADCAST, messageId, wParam)
    
    print("PostMessage ok")

if __name__ == "__main__":
    main()
