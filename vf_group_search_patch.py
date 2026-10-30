# -*- coding: utf-8 -*-
# VF_GROUP_SEARCH_V1: STEP1 グループをbigGenreでoptgroupまとめ + グループ/キャラ検索フィルタ追加
# 対象: C:\AI\ComfyUI\dashboard.html
import io, re, sys, shutil, datetime

P = r'C:\AI\ComfyUI\dashboard.html'
t = io.open(P, encoding='utf-8', errors='strict').read()

if 'VF_GROUP_SEARCH_V1' in t:
    print('already patched'); sys.exit(0)

bak = P + '.bak_vfgs_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(P, bak)
print('backup:', bak)

# ---- 1) HTML: 検索input追加（グループlabel行とキャラlabel行） ----
old_html = '<label style="font-size:11px;color:#94a3b8">グループ</label><select id="vf_group" onchange="VF.fillChars()"'
new_html = ('<label style="font-size:11px;color:#94a3b8">グループ <input id="vf_groupSearch" type="text" placeholder="🔍検索" oninput="VF.rebuildGroupSel()" '
            'style="width:110px;height:20px;background:#0d0d1a;color:#e5e7eb;border:1px solid #374151;border-radius:4px;padding:0 6px;font-size:11px;margin-left:6px"></label>'
            '<select id="vf_group" onchange="VF.fillChars()"')
assert old_html in t, 'HTML group anchor not found'
t = t.replace(old_html, new_html, 1)

old_html2 = '<label style="font-size:11px;color:#94a3b8">キャラ <span id="vf_charCount" style="color:#6b7280"></span></label>'
new_html2 = ('<label style="font-size:11px;color:#94a3b8">キャラ <span id="vf_charCount" style="color:#6b7280"></span> '
             '<input id="vf_charSearch" type="text" placeholder="🔍検索" oninput="VF.fillChars()" '
             'style="width:110px;height:20px;background:#0d0d1a;color:#e5e7eb;border:1px solid #374151;border-radius:4px;padding:0 6px;font-size:11px;margin-left:6px"></label>')
assert old_html2 in t, 'HTML char anchor not found'
t = t.replace(old_html2, new_html2, 1)

# ---- 2) JS: グループ構築を optgroup(bigGenre) + 検索対応に差し替え ----
old_js = '''      var gsel = document.getElementById('vf_group');
      if (gsel && gsel.options.length === 0) {
        var all = VF.allChars();
        var defs = (window.CHAR_GROUP_DEFS||[]).map(function(g){ var n = all.filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }).length; return {g:g,n:n}; }).filter(function(x){return x.n>0;});
        defs.sort(function(a,b){ return (a.g.label||'').localeCompare(b.g.label||'','ja'); });
        gsel.innerHTML = defs.map(function(x){ return '<option value="'+x.g.key+'">'+x.g.label+' ('+x.n+'体)</option>'; }).join('');
        var saved = localStorage.getItem('_vf_group'); if (saved) gsel.value = saved;
        VF.fillChars();
      }'''
new_js = '''      var gsel = document.getElementById('vf_group');
      if (gsel && gsel.options.length === 0) {
        // [VF_GROUP_SEARCH_V1] bigGenreごとにoptgroupでまとめ + 検索フィルタ
        var all = VF.allChars();
        VF._groupDefs = (window.CHAR_GROUP_DEFS||[]).map(function(g){ var n = all.filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }).length; return {g:g,n:n}; }).filter(function(x){return x.n>0;});
        VF._groupDefs.sort(function(a,b){ return (a.g.label||'').localeCompare(b.g.label||'','ja'); });
        VF.rebuildGroupSel(true);
      }'''
assert old_js in t, 'JS group-build anchor not found'
t = t.replace(old_js, new_js, 1)

# rebuildGroupSel 関数を fillChars の直前に追加
old_fill = '''    fillChars: function(){
      var key = document.getElementById('vf_group').value; localStorage.setItem('_vf_group', key);'''
new_fill = '''    rebuildGroupSel: function(isInit){
      // [VF_GROUP_SEARCH_V1] 検索語でフィルタし、bigGenre別optgroupで描画
      var gsel = document.getElementById('vf_group'); if(!gsel || !VF._groupDefs) return;
      var q = ((document.getElementById('vf_groupSearch')||{}).value||'').trim().toLowerCase();
      var defs = VF._groupDefs.filter(function(x){ return !q || (x.g.label||'').toLowerCase().indexOf(q)>=0 || (x.g.key||'').toLowerCase().indexOf(q)>=0 || (x.g.bigGenre||'').toLowerCase().indexOf(q)>=0; });
      var prev = gsel.value || localStorage.getItem('_vf_group');
      var byGenre = {}; var order = [];
      defs.forEach(function(x){ var bg = x.g.bigGenre || '📂 その他'; if(!byGenre[bg]){ byGenre[bg]=[]; order.push(bg); } byGenre[bg].push(x); });
      order.sort(function(a,b){ return a.localeCompare(b,'ja'); });
      gsel.innerHTML = order.map(function(bg){
        return '<optgroup label="'+bg+' ('+byGenre[bg].length+'グループ)">' + byGenre[bg].map(function(x){ return '<option value="'+x.g.key+'">'+x.g.label+' ('+x.n+'体)</option>'; }).join('') + '</optgroup>';
      }).join('');
      if (prev && defs.some(function(x){return x.g.key===prev;})) gsel.value = prev;
      VF.fillChars();
    },
    fillChars: function(){
      var key = document.getElementById('vf_group').value; localStorage.setItem('_vf_group', key);'''
assert old_fill in t, 'fillChars anchor not found'
t = t.replace(old_fill, new_fill, 1)

# fillChars にキャラ検索フィルタを追加
old_chars = '''      var chars = g ? VF.allChars().filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }) : [];
      var csel = document.getElementById('vf_char');'''
new_chars = '''      var chars = g ? VF.allChars().filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }) : [];
      // [VF_GROUP_SEARCH_V1] キャラ名検索フィルタ
      var cq = ((document.getElementById('vf_charSearch')||{}).value||'').trim().toLowerCase();
      if (cq) chars = chars.filter(function(t){ return (t.label||'').toLowerCase().indexOf(cq)>=0 || (t.id||'').toLowerCase().indexOf(cq)>=0; });
      var csel = document.getElementById('vf_char');'''
assert old_chars in t, 'fillChars chars anchor not found'
t = t.replace(old_chars, new_chars, 1)

# ---- 3) version +1 ----
m = re.search(r'name="version" content="(\d+)"', t)
if m:
    old_v = m.group(1); new_v = str(int(old_v)+1)
    t = t.replace('content="'+old_v+'"', 'content="'+new_v+'"')
    print('version:', old_v, '->', new_v)
else:
    print('version meta not found (skip)')

io.open(P, 'w', encoding='utf-8').write(t)
print('patched OK')
