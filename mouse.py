import win32con, win32api

def move(x, y):
    win32api.SetCursorPos((x, y))

def click(x, y):
    move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
