"""
AUTO_RELOAD_V1を正しい位置（本物の</body>直前）に移動。
誤挿入されたポップアップHTML内の<script>を除去。
"""
import re, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
shutil.copy2(path, path + '.bak_ar_fix')

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

AUTO_RELOAD_JS = """<script>
// [AUTO_RELOAD_V1] APIサーバーのdashboard.htmlバージョンが変わったら自動リロード
(function() {
  var _arCurVer = document.querySelector('meta[name="version"]') ? document.querySelector('meta[name="version"]').content : '0';
  function _arCheck() {
    fetch('/api/dashboard_version', {cache:'no-store'})
      .then(function(r) { return r.json(); })
      .then(function(d) {
        var v = d.version || d.ver || '0';
        if (v !== '0' && v !== _arCurVer) {
          console.log('[AUTO_RELOAD] version changed', _arCurVer, '->', v, '-> reloading');
          location.reload(true);
        }
      })
      .catch(function() {});
  }
  setInterval(_arCheck, 10000);
})();
</script>"""

# 1. 既存のAUTO_RELOAD_V1ブロックを全部除去
content = re.sub(
    r'<script>\s*//\s*\[AUTO_RELOAD_V1\].*?</script>\s*',
    '',
    content,
    flags=re.DOTALL
)
print('既存AUTO_RELOAD除去完了')

# 2. 本物の</body>（最後の</body>）の直前に挿入
last_body = content.rfind('</body>')
if last_body == -1:
    print('ERROR: </body>が見つからない')
    sys.exit(1)

content = content[:last_body] + AUTO_RELOAD_JS + '\n' + content[last_body:]
print('AUTO_RELOAD_V1を最終</body>直前に挿入')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('完了')
