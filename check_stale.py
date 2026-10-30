import os, datetime
bid = os.stat(r'C:\GensparkClaw\kujira-support\.next\BUILD_ID').st_mtime
src = max(os.stat(os.path.join(r,f)).st_mtime for r,ds,fs in os.walk(r'C:\GensparkClaw\kujira-support\src') for f in fs)
print('BUILD:', datetime.datetime.fromtimestamp(bid))
print('SRC  :', datetime.datetime.fromtimestamp(src))
print('STALE:', src > bid)
