try:
    import win32com.client
    print('pywin32 OK')
except ImportError:
    print('NOT FOUND')
