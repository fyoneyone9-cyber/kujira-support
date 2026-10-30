"""
dashboard.htmlに自動リロードポーリングを追加。
APIサーバーのバージョンが変わったら自動でlocation.reload()する。
"""
import re, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
shutil.copy2(path, path + '.bak_autoreload')

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 現在のバージョン取得
m = re.search(r"content=['\"]([0-9]+)['\"] name=['\"]version['\"]", content)
if not m:
    m = re.search(r"name=['\"]version['\"] content=['\"]([0-9]+)['\"]", content)
old_ver = m.group(1) if m else '0'
import time
new_ver = str(int(time.time()))
print(f'version: {old_ver} -> {new_ver}')

# バージョン更新
content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)

# 自動リロードスクリプトを</body>直前に挿入
AUTO_RELOAD_JS = f'''
<script>
// [AUTO_RELOAD_V1] APIサーバーのdashboard.htmlバージョンが変わったら自動リロード
(function() {{
  var _arCurVer = '{new_ver}';
  var _arFail = 0;
  function _arCheck() {{
    fetch('/api/dashboard_version', {{cache:'no-store'}})
      .then(function(r) {{ return r.json(); }})
      .then(function(d) {{
        _arFail = 0;
        var v = d.version || d.ver || '0';
        if (v !== '0' && v !== _arCurVer) {{
          console.log('[AUTO_RELOAD] version changed', _arCurVer, '->', v, '-> reloading');
          location.reload(true);
        }}
      }})
      .catch(function() {{ _arFail++; }});
  }}
  // 10秒ごとにポーリング（生成中は負荷をかけない）
  setInterval(_arCheck, 10000);
}})();
</script>
'''

if '[AUTO_RELOAD_V1]' in content:
    print('既に追加済み')
else:
    content = content.replace('</body>', AUTO_RELOAD_JS + '</body>', 1)
    print('AUTO_RELOAD_V1 追加')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('完了')
