import sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
shutil.copy2(path, path + '.bak_newline_fix')
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# </pre>の後の生改行を除去（文字列リテラル内）
old = "+'</pre>\n</body></html>')"
new = "+'</pre></body></html>')"
if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('修正完了')
else:
    idx = content.find("+'</pre>")
    print('ターゲット見つからず、周辺:', repr(content[idx:idx+50]))
