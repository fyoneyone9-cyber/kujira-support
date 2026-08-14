new_block_top = '''      {/* 参考資料リンク */}
      <div className="mb-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-sm text-slate-300 font-bold mb-4">📁 参考資料</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">🟠</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-orange-300 transition-colors">HubSpot 架電リスト</p>
              <p className="text-slate-400 text-sm">取引一覧（楽天トラベルフィルター済）</p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">📹</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">Zoom マイホーム</p>
              <p className="text-slate-400 text-sm">架電・セミナー用 Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📊</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル（スプレッドシート）</p>
              <p className="text-slate-400 text-sm">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📋</span>
            <div>
              <p className="text-white text-sm font-semibold group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-400 text-sm">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>

'''

# クリーンなgit版をutf-8-sigで読む（PowerShellのOut-FileはUTF-8 BOM付き）
with open(r'C:\Users\fyone\Desktop\teleapo_clean.tsx', 'r', encoding='utf-8-sig') as f:
    c = f.read()

# タブコメントの直前に参考資料を挿入
insert_after = '      {/* Tabs */}'
if insert_after in c:
    c = c.replace(insert_after, new_block_top + insert_after, 1)
    with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'w', encoding='utf-8') as f:
        f.write(c)
    print('done, lines:', c.count('\n'))
else:
    print('marker not found')
    # 代替マーカーを探す
    import re
    m = re.search(r'\{/\* Tab', c)
    if m:
        print('found at:', m.start(), repr(c[m.start():m.start()+30]))
