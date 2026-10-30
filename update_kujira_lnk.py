import win32com.client, os

PYTHON = r'C:\Users\fyone\anaconda3\python.exe'
SCRIPT = r'C:\GensparkClaw\kujira-support\kujira_start.py'
LNK    = r'C:\Users\fyone\Desktop\★KUJIRA★.lnk'

shell = win32com.client.Dispatch('WScript.Shell')
sc = shell.CreateShortCut(LNK)
sc.TargetPath = PYTHON
sc.Arguments  = f'"{SCRIPT}"'
sc.WorkingDirectory = r'C:\GensparkClaw\kujira-support'
sc.IconLocation = r'C:\Windows\System32\shell32.dll,23'
sc.WindowStyle  = 1
sc.Save()
print(f'Updated: {LNK}')
print(f'  -> {PYTHON} "{SCRIPT}"')
