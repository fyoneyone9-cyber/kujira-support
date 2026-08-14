import subprocess, re

blob_hash = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'ls-tree', 'HEAD', 'src/app/(app)/teleapo/page.tsx'],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True, text=True
).stdout.split()[2]

raw = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'cat-file', 'blob', blob_hash],
    cwd=r'C:\Users\fyone\Desktop\kujira-support', capture_output=True
).stdout

c = raw.decode('utf-8', errors='replace')

# 参考資料ブロックを抽出（mt-6のdivから閉じdivまで）
m = re.search(r'\s*\{/\* 参考資料リンク \*/\}.*?</div>\s*\n\s*</div>\s*\n\s*\)', c, re.DOTALL)
if not m:
    # コメントなし版を探す
    idx = c.find('HubSpot 架電リスト')
    # その周辺のdivブロックを特定
    start = c.rfind('\n      <div', 0, idx)
    # 閉じdiv4つ分を探す
    end = c.find('</div>\n      </div>\n    </div>\n  )\n}', idx)
    if end > 0:
        end = end + len('</div>\n      </div>')
    print(f'block: {start} - {end}')
    block = c[start:end]
    print('block preview:', block[:100])
else:
    start, end = m.start(), m.end()
    block = m.group()
    print('found by comment')

# タブコメント直前に移動
sanko_block = '''

      {/* 参考資料リンク */}
      <div className="mb-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-sm text-slate-300 font-bold mb-4">\U0001f4c1 参考資料</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">\U0001f7e0</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-orange-300 transition-colors">HubSpot 架電リスト</p>
              <p className="text-slate-400 text-sm">取引一覧（楽天トラベルフィルター済）</p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">\U0001f4f9</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">Zoom マイホーム</p>
              <p className="text-slate-400 text-sm">架電・セミナー用 Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">\U0001f4ca</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル（スプレッドシート）</p>
              <p className="text-slate-400 text-sm">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">\U0001f4cb</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-400 text-sm">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>
'''

# 元の参考資料ブロックを探してmtをmbに変えて位置を特定
old_sanko = re.search(r'\n\s*\{/\* 参考資料リンク \*/\}[\s\S]+?</div>\n      </div>', c)
if old_sanko:
    # 削除
    c = c[:old_sanko.start()] + c[old_sanko.end():]
    print('old block removed')

# タブコメントの直前に挿入
marker = '      {/* Tabs */}'
if marker in c:
    c = c.replace(marker, sanko_block.lstrip('\n') + '\n' + marker, 1)
    print('inserted before Tabs')
else:
    print('Tabs marker not found')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('saved, lines:', c.count('\n'))
