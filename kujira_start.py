"""
KUJIRA起動スクリプト
1. next build（変更があればビルド）
2. start_server_loop.bat でサーバー起動
3. ブラウザで http://localhost:3001 を開く
"""
import subprocess, os, sys, time, datetime

PROJECT = r'C:\GensparkClaw\kujira-support'
NEXT = os.path.join(PROJECT, r'node_modules\.bin\next.cmd')
LOOP_BAT = os.path.join(PROJECT, 'start_server_loop.bat')
URL = 'http://localhost:3001'

def log(msg):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {msg}')

def is_stale():
    """BUILD_IDよりsrcの.tsx/.tsが新しければTrue"""
    import os
    bid_path = os.path.join(PROJECT, '.next', 'BUILD_ID')
    if not os.path.exists(bid_path):
        return True
    build_mtime = os.stat(bid_path).st_mtime
    latest = 0
    for root, dirs, files in os.walk(os.path.join(PROJECT, 'src')):
        for f in files:
            if f.endswith(('.tsx', '.ts', '.css')):
                mt = os.stat(os.path.join(root, f)).st_mtime
                if mt > latest:
                    latest = mt
    return latest > build_mtime

def port_in_use(port=3001):
    import socket
    with socket.socket() as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

# 1. ビルド判定
if is_stale():
    log('未反映の変更あり → ビルド開始...')
    r = subprocess.run([NEXT, 'build'], cwd=PROJECT, shell=False)
    if r.returncode != 0:
        log('ビルド失敗！終了します')
        input('Enterで閉じる')
        sys.exit(1)
    log('ビルド完了')
else:
    log('変更なし → ビルドスキップ')

# 2. サーバー起動（起動済みならスキップ）
if port_in_use():
    log('サーバーはすでに起動中')
else:
    log('サーバー起動...')
    subprocess.Popen(['cmd.exe', '/c', LOOP_BAT], creationflags=subprocess.CREATE_NEW_CONSOLE)
    for _ in range(30):
        time.sleep(1)
        if port_in_use():
            break
    if port_in_use():
        log('サーバー起動確認OK')
    else:
        log('警告: サーバー起動確認できず（続行）')

# 3. ブラウザを開く
log(f'ブラウザで {URL} を開きます')
os.startfile(URL)
log('起動完了')
