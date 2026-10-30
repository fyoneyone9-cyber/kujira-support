import shutil, os, glob

src_dir = r'C:\Users\fyone\Downloads'
dst_dir = r'C:\GensparkClaw\kujira-support\docs\hearing-sheet'
os.makedirs(dst_dir, exist_ok=True)

files = glob.glob(os.path.join(src_dir, '*.csv'))
copied = []
for f in files:
    name = os.path.basename(f)
    if 'hearing' in name.lower() or 'ヒアリング' in name:
        shutil.copy2(f, os.path.join(dst_dir, name))
        copied.append(name)

print(f'Copied {len(copied)} files:')
for c in copied:
    print(' ', c)
