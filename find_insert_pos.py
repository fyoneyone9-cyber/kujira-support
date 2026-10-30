import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
# aerith S1追加位置: char_kakuseizai_jk_C の push( を探してその直後
jkc = content.find("char_kakuseizai_jk_C")
if jkc < 0: print("jk_C not found"); sys.exit()
line_num = content[:jkc].count('\n') + 1
print("jk_C at line:", line_num)
# jk_CのpushブロックのendをHTMLで見つける
# push({ ... }); のendを探す
# jkc から前向きに }); を探す
end_pos = content.find('});', jkc)
end_line = content[:end_pos].count('\n') + 1
print("End of jk_C block (});\\ at line:", end_line, "pos:", end_pos)
print("Context:", repr(content[end_pos:end_pos+30]))
