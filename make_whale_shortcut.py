# -*- coding: utf-8 -*-
import os, struct, subprocess, sys

# 1. 🐳アイコンをPillowで生成
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pillow', '-q'])
    from PIL import Image, ImageDraw, ImageFont

ico_path = r'C:\Users\fyone\Desktop\kujira.ico'

# 256x256 の画像に🐳を描く
img = Image.new('RGBA', (256, 256), (30, 30, 50, 255))
draw = ImageDraw.Draw(img)

# フォントを探す（絵文字対応）
font = None
for fp in [
    r'C:\Windows\Fonts\seguiemj.ttf',   # Segoe UI Emoji
    r'C:\Windows\Fonts\seguisym.ttf',
]:
    if os.path.exists(fp):
        try:
            font = ImageFont.truetype(fp, 180)
            break
        except:
            pass

if font:
    # テキストを中央に配置
    draw.text((128, 128), '\U0001f433', font=font, anchor='mm')
else:
    # フォールバック: シンプルな青丸
    draw.ellipse([20, 20, 236, 236], fill=(0, 120, 255, 255))

# マルチサイズicoとして保存
sizes = [256, 128, 64, 48, 32, 16]
imgs = [img.resize((s, s), Image.LANCZOS) for s in sizes]
imgs[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes],
             append_images=imgs[1:])
print(f'Icon saved: {ico_path}')

# 2. ショートカットを作成
import win32com.client  # pywin32
shell = win32com.client.Dispatch('WScript.Shell')
lnk_path = r'C:\Users\fyone\Desktop\KUJIRA起動.lnk'
sc = shell.CreateShortcut(lnk_path)
sc.TargetPath = r'C:\Users\fyone\Desktop\KUJIRA_Start.bat'
sc.WorkingDirectory = r'C:\Users\fyone\Desktop'
sc.IconLocation = ico_path
sc.Description = 'KUJIRA Support System \u8d77\u52d5'
sc.Save()
print(f'Shortcut saved: {lnk_path}')
