
(function(){

  // VF_STEP4_JS: STEP4 設定保存・続きから・フォルダ開く
  window.s4save = function() {
    var s = JSON.parse(localStorage.tkVfWan||'{}');
    ['s4wf','s4len','s4motion','s4steps','s4res'].forEach(function(id,i){
      var el = document.getElementById(id); if(el) s[['wf','len','motion','steps','res'][i]] = el.value;
    });
    localStorage.tkVfWan = JSON.stringify(s);
    // 既存 tkVfWan UI にも反映
    var map = {tkVfWanWf:'wf',tkVfWanLen:'len',tkVfWanMotion:'motion',tkVfWanSteps:'steps',tkVfWanRes:'res'};
    Object.keys(map).forEach(function(id){ var el=document.getElementById(id); if(el&&s[map[id]]) el.value=s[map[id]]; });
  };
  window.s4restore = function() {
    var s = JSON.parse(localStorage.tkVfWan||'{}');
    s.len='161';
    var map = {s4wf:'wf',s4len:'len',s4motion:'motion',s4steps:'steps',s4res:'res'};
    Object.keys(map).forEach(function(id){ var el=document.getElementById(id); if(el&&s[map[id]]) el.value=s[map[id]]; });
  };
  window.s4resume = function() {
    // [VF_RUNNING_VIDEO_BLOCK_V1 2026-10-05] 連続画像生成中は動画の「続きから」もブロック
    // [VF_RUNNING_VIDEO_BLOCK_FIX_V1 2026-10-06] ユーザー報告:「停止してるのにこれ出て
    // 動画つくれない」。VF.stop()は_stopフラグを立てるだけで、実行中ループが現在の
    // コマ処理を終えるまで_runningはtrueのまま残る(非同期の遅延)。停止要求済み(_stop)
    // なら動画生成をブロックしない。またブロック時もalert()でなくログのみに変更。
    if (window.VF && VF._running && !VF._stop) { console.warn('[VF_VIDEO] 画像の連続生成中のため動画生成をスキップ'); if (typeof window._opLog === 'function') window._opLog('warn', '⚠️ 画像の連続生成中です。動画生成は連続生成が完了（または停止）してから実行してください。'); return; }
    var rs = ((window.VF&&VF._results)||[]).filter(function(r){return r.ok&&r.image_path&&!r.video;});
    if(!rs.length){alert('動画未生成のコマはありません');return;}
    if(!confirm(rs.length+'件の動画未生成コマを再生成します。よろしいですか？'))return;
    window._tkVfWanDone = window._tkVfWanDone||new Set();
    rs.forEach(function(r){window._tkVfWanDone.delete(r.image_path);});
    if(window.tkVfWanRun) tkVfWanRun();
  };
  window.s4openFolder = function(path) {
    fetch((window.API||location.origin)+'/api/open-folder',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:path})}).catch(function(){});
  };
  // VF_VIDEO_GALLERY_SIMPLE: 画像ギャラリー横の動画ギャラリー更新
  window.vfUpdateVideoGallery = function() {
    var vg = document.getElementById('vf_vg_grid');
    var wrap = document.getElementById('vf_video_gallery');
    var cnt = document.getElementById('vf_vg_count');
    if(!vg || !wrap) return;
    var rs = (window.VF && VF._results) || [];
    var withVideo = rs.filter(function(r){ return r.ok && r.video; });
    // 動画ゼロなら非表示
    wrap.style.display = withVideo.length ? 'flex' : 'none';
    if(cnt) cnt.textContent = '(' + withVideo.length + '本)';
    var seen = {};
    var API2 = window.API || location.origin;
    withVideo.forEach(function(r){
      var key = 'vfvg_' + r.idx; seen[key] = 1;
      var vurl = API2 + (r.video.startsWith('/') ? r.video : '/output/videos/' + r.video.split('/').pop());
      var iurl = r.image_path ? (r.image_path.indexOf('/output/')===0 ? API2+r.image_path : API2+'/api/image?path='+encodeURIComponent(r.image_path)) : '';
      var sig = vurl;
      var card = document.getElementById(key);
      if(card && card.dataset.sig === sig) return;
      var h = '<div style="position:relative">'
        + '<video src="'+vurl+'" controls muted playsinline loop style="width:100%;aspect-ratio:16/9;object-fit:contain;background:#000;display:block" preload="metadata"></video>'
        + (iurl ? '<img src="'+iurl+'" style="position:absolute;top:4px;left:4px;width:36px;height:48px;object-fit:cover;border-radius:3px;border:1px solid #374151;opacity:.85">' : '')
        + '</div>'
        + '<div style="padding:4px 8px;font-size:11px;color:#cbd5e1;display:flex;gap:4px;align-items:center">'
        + '<b style="color:#93c5fd">' + (r.idx+1) + '</b>'
        + '<span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + (r.label||'') + '</span>'
        + '<a href="'+vurl+'" download style="font-size:10px;padding:1px 7px;background:#065f46;color:#6ee7b7;border:1px solid #047857;border-radius:3px;text-decoration:none;white-space:nowrap">⬇DL</a>'
        + '<button onclick="vfDeleteVideo(\''+r.idx+'\')" style="font-size:10px;padding:1px 6px;background:#3b0a0a;color:#fca5a5;border:1px solid #7f1d1d;border-radius:3px;cursor:pointer">🗑</button>'
        + '</div>';
      if(!card){ card=document.createElement('div'); card.id=key; card.style.cssText='background:#0b1220;border:1px solid #1e3a5f;border-radius:8px;overflow:hidden'; }
      card.dataset.sig=sig; card.dataset.idx=r.idx; card.innerHTML=h;
      var placed=false;
      for(var c=vg.firstElementChild;c;c=c.nextElementSibling){ if(c!==card&&parseInt(c.dataset.idx||'-1',10)>r.idx){vg.insertBefore(card,c);placed=true;break;} }
      if(!placed&&card.parentNode!==vg) vg.appendChild(card);
    });
    Array.prototype.slice.call(vg.children).forEach(function(c){ if(!seen[c.id]) c.remove(); });
  };
  // 進捗フック
  (function(){
        function hookRun(){
      if(!window.tkVfWanRun||window._s4Hooked) return;
      window._s4Hooked = true;
      var orig = window.tkVfWanRun;
      window.tkVfWanRun = async function(){
        var total = ((window.VF&&VF._results)||[]).filter(function(r){return r.ok&&r.image_path&&!r.video;}).length;
        var wrap=document.getElementById('s4progWrap'),bar=document.getElementById('s4progBar'),
            lbl=document.getElementById('s4progLabel'),txt=document.getElementById('s4progText');
        var vst=document.getElementById('vf_video_status'),vbw=document.getElementById('vf_video_bar_wrap'),vb=document.getElementById('vf_video_bar');
        if(total>0){
          if(wrap) wrap.style.display='flex';
          if(vbw){ vbw.style.display='block'; if(vst) vst.style.display='block'; }
        }
        var timer = setInterval(function(){
          var done=((window.VF&&VF._results)||[]).filter(function(r){return r.video;}).length;
          var pct=total>0?Math.round(done/total*100):0;
          if(bar) bar.style.width=pct+'%';
          if(txt) txt.textContent=done+' / '+total;
          if(lbl) lbl.textContent=done>=total?'✅ 動画生成完了！':'🎬 動画生成中 ('+pct+'%)';
          if(vb) vb.style.width=pct+'%';
          if(vst) vst.textContent=done>=total?'✅ 動画完了 '+done+'/'+total+' 本':'🎬 動画生成中 '+done+'/'+total+' ('+pct+'%)';
        },1500);
        try{ return await orig.apply(this,arguments); }
        finally{
          clearInterval(timer);
          setTimeout(function(){
            if(wrap) wrap.style.display='none';
            if(vbw){ vbw.style.display='none'; if(vst) vst.style.display='none'; }
            if(window.vfUpdateVideoGallery) vfUpdateVideoGallery();
          },5000);
        }
      };
    }
    setInterval(hookRun,1200);
    // [VF_RUNNING_TALK_SYNC_V1 2026-10-05] ユーザー指摘「動画生成のリクエストが飛ぶけど
    // 連続作成中はやめて頂きたい」「slideshow(3097/talk_server 3004)が悪さしてるかも」。
    // 根本原因: talk_server.pyの自動ループがoutput/single_*.pngを監視し、VF連続生成中の
    // 新規画像にも反応してComfyUIへ追加の口パク/まばたき生成リクエストを送信していた。
    // VF._runningの状態を5秒おきにtalk_server(3004)へ伝え、連続生成中はそのループを
    // 一時停止させる(失敗しても握り潰す=talk_server未起動でもVF動作に影響させない)。
    (function(){
      var _lastSent = null;
      setInterval(function(){
        var running = !!(window.VF && VF._running);
        if (running === _lastSent) return; // 状態変化時のみ送信(負荷軽減)
        _lastSent = running;
        fetch('http://127.0.0.1:3004/talk/vf_busy?on=' + running, {method:'POST'}).catch(function(){});
      }, 3000);
      // 状態継続中も120秒タイムアウト対策で定期的に再送(talk_server側のget_vf_busyの自動解除を防ぐ)
      setInterval(function(){
        if (window.VF && VF._running) {
          fetch('http://127.0.0.1:3004/talk/vf_busy?on=true', {method:'POST'}).catch(function(){});
        }
      }, 60000);
    })();
  })();
  document.addEventListener('DOMContentLoaded',function(){setTimeout(function(){if(window.s4restore)s4restore();},800);});
  if(document.readyState!=='loading') setTimeout(function(){if(window.s4restore)s4restore();},800);

  var VF = window.VF = {
    _running: false, _stop: false, _results: [],
    // [VF_SCRIPT_MODE_V1 2026-10-10] 台本由来漫画作成モード（既存キャラのみ対応）
    // #pageList の実体DOMを物理的にVFタブ内のスロットへ移動して使い回す。
    // renderPageList/generateSinglePanel等の既存ロジックは一切変更しない。
    toggleScriptMode: function(){
      var wrap = document.getElementById('vf_scriptModeWrap');
      if (!wrap) return;
      var opening = wrap.style.display === 'none';
      wrap.style.display = opening ? 'block' : 'none';
      var btn = document.getElementById('vf_scriptModeBtn');
      if (btn) btn.textContent = opening ? '📜 台本モードを閉じる' : '📜 ここで台本モードを開く（既存キャラのみ対応）';
      var pageList = document.getElementById('pageList');
      var slot = document.getElementById('vf_scriptModeSlot');
      if (!pageList || !slot) return;
      if (opening) {
        // 元の位置を覚えておいて、スロットへ移動
        if (!pageList.__vfOrigParent) {
          pageList.__vfOrigParent = pageList.parentElement;
          pageList.__vfOrigNext = pageList.nextSibling;
        }
        slot.appendChild(pageList);
      } else {
        // 元の位置へ戻す
        if (pageList.__vfOrigParent) {
          if (pageList.__vfOrigNext && pageList.__vfOrigNext.parentElement === pageList.__vfOrigParent) {
            pageList.__vfOrigParent.insertBefore(pageList, pageList.__vfOrigNext);
          } else {
            pageList.__vfOrigParent.appendChild(pageList);
          }
        }
      }
    },
    runScriptAnalyze: async function(){
      var ta = document.getElementById('vf_scriptInput');
      var statusEl = document.getElementById('vf_scriptModeStatus');
      if (!ta || !ta.value.trim()) { if (statusEl) statusEl.textContent = '台本を入力してください'; return; }
      // [VF_SCRIPT_INPUT_GUARD_V1 2026-10-10] ユーザー報告:「入力した台本が生成中に別の
      // 文字(前回のサンプル等)に上書きされる」。原因特定には至らなかったが、解析中に
      // ta.value が何らかの理由で変化しても元の入力を失わないよう、実行開始時点の値を
      // 退避し、処理後に消えていたら復元するガードを追加(防御的)。連打防止もあわせて実施。
      if (this._scriptAnalyzeRunning) { if (statusEl) statusEl.textContent = '⏳ 既に解析中です...'; return; }
      this._scriptAnalyzeRunning = true;
      var _savedInput = ta.value;
      var runBtn = document.querySelector('#vf_scriptModeWrap button[onclick="VF.runScriptAnalyze()"]');
      if (runBtn) runBtn.disabled = true;
      // 既存の「台本・設定」タブの #script textarea に流し込んでから、既存の自動解析関数をそのまま呼ぶ
      // (プロンプト生成/話者マッピング等のロジックを二重実装しないため)
      var mainScript = document.getElementById('script');
      if (mainScript) mainScript.value = _savedInput;
      if (statusEl) statusEl.textContent = '🔄 解析中...';
      // [VF_SCRIPT_MODE_NO_TAB_SWITCH_V1 2026-10-10] ユーザー報告:「ページ一覧の各コマが
      // 表示できなくなってる」の真因: autoDetectChars()内部が解析完了時に「ページ一覧」タブへ
      // 強制切り替えする。VFの台本モードでは#pageListを既にVFタブ内へ移動済みのため、
      // タブ切り替えされると移動元の「ページ一覧」タブが空に見えてしまう。フラグで抑制する。
      window._vfScriptModeActive = true;
      try {
        if (typeof window.autoDetectChars === 'function') {
          await window.autoDetectChars();
        }
        if (statusEl) statusEl.textContent = '✅ 解析完了（既存キャラが未登録の話者は容姿不明のため反映されません）';
      } catch(e) {
        if (statusEl) statusEl.textContent = '❌ 解析失敗: ' + (e && e.message ? e.message : e);
      } finally {
        // ta.value が解析処理中に何らかの理由で消えていた場合、入力していた内容を復元する防御
        if (ta && !ta.value.trim() && _savedInput) ta.value = _savedInput;
        this._scriptAnalyzeRunning = false;
        window._vfScriptModeActive = false;
        if (runBtn) runBtn.disabled = false;
      }
    },
    init: function(){
      // checkpoint 一覧: メイン select をコピー
      var dst = document.getElementById('vf_ckpt');
      if (dst && dst.options.length <= 1) {
        var PRESETS = [
          ['moody_krea2_v8','🥇No.1 MoodyV8 SE【実写】総合画質トップ(肌質・陰影・光)※構図は複雑すぎると四肢崩壊→neg対策済'],
          ['realdream_krea2v1','🥈No.2 RealDream Krea2【実写】日本人顔の自然さNo.1・破綻率低い'],
          ['redqw21_v3','🥉No.3 RedQW21 V3【実写】無修正表現力トップ・10stepで速い(顔は洋風寄り→日本人顔タグ対策済)'],
          ['krea2_darkbeast','No.5 DarkBeast★【実写】ダーク系・夜シーンの雰囲気最強'],
          ['krea2_snofs','No.6 SNOFS【実写】透明感・清潔感(ソフト系に最適)'],
          ['moody_moss_v2','No.6.5 Moody MOSS V2【実写】新アーキMOSS・Moodyスタイル(25step)'],
          ['redqw21_unlocked','No.7 RedQW21 V2【実写】8step最速で量産向き(細部は甘い)'],
          ['pornmaster_klein','No.9 PornMaster Klein【実写NSFW】群像・構図力◎9step(肌CG寄り→対策済)'],
          ['redqw21_unlocked_v1','No.10 RedQW21 V1【実写】25stepで精細だが約90秒'],
          ['redcraft_h3k2_30','No.11 RedCraft v30【実写】v40の安定版(攻め幅狭い)'],
          ['realdream_anima','No.12 RealDream Anima【実写/アニメ】2.5D両対応の器用貧乏'],
          ['pony_photo','No.15 Pony実写 旧世代・体位語彙は豊富'],
          ['waisnack_real','No.16 WAI実写【複数対応】LoRA欠損中で本来の画質出ず'],
          ['waisnack_anime','🎨アニメNo.1 WAIアニメ 塗り安定・キャラ再現◎'],
          ['pony_real','🎨アニメNo.2 Ponyアニメ NSFWアニメ塗り'],
          ['unholy_desire','🎨アニメNo.3 Unholy ダーク系アニメ特化']
        ];
        dst.innerHTML = '<option value="">(現在のプリセットのまま)</option>' + PRESETS.map(function(p){ var ok = (typeof STYLE_PRESETS==='undefined') || !!STYLE_PRESETS[p[0]]; return '<option value="'+p[0]+'"'+(ok?'':' disabled')+'>'+p[1]+(ok?'':' (未定義)')+'</option>'; }).join('');
        var savedP = localStorage.getItem('_vf_preset') || localStorage.getItem('_manualPresetKey') || '';
        if (savedP && Array.from(dst.options).some(function(o){return o.value===savedP;})) dst.value = savedP;
      }
      // グループ一覧 (CHAR_GROUP_DEFS + 体数)
      var gsel = document.getElementById('vf_group');
      if (gsel && gsel.options.length === 0) {
        // [VF_GROUP_SEARCH_V1] bigGenreごとにoptgroupでまとめ + 検索フィルタ
        var all = VF.allChars();
        VF._groupDefs = (window.CHAR_GROUP_DEFS||[]).map(function(g){ var n = all.filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }).length; return {g:g,n:n}; }).filter(function(x){return x.n>0;});
        VF._groupDefs.sort(function(a,b){ return (a.g.label||'').localeCompare(b.g.label||'','ja'); });
        VF.rebuildGroupSel(true);
      }
      VF.renderGallery();
      try { var rb=document.getElementById('vf_runBtn'), sb=document.getElementById('vf_stopBtn'); if(rb){rb.disabled=!!VF._running;rb.style.opacity=VF._running?.5:1;} if(sb){sb.disabled=!VF._running;sb.style.opacity=VF._running?1:.5;} } catch(e){}
    },
    allChars: function(){
      var a = (typeof CHAR_TEMPLATES!=='undefined') ? Object.values(CHAR_TEMPLATES).flat() : [];
      var b = (window.CHAR_TEMPLATES && window.CHAR_TEMPLATES!==CHAR_TEMPLATES) ? Object.values(window.CHAR_TEMPLATES).flat() : [];
      var seen = {};
      return a.concat(b).filter(function(t){ if(!t||typeof t!=='object'||!t.id||!t.label||t.hidden||t.gender==='narrator') return false; if(seen[t.id]) return false; seen[t.id]=1; return true; });
    },
    rebuildGroupSel: function(isInit){
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
      var key = document.getElementById('vf_group').value; localStorage.setItem('_vf_group', key);
      var g = (window.CHAR_GROUP_DEFS||[]).find(function(x){return x.key===key;});
      var chars = g ? VF.allChars().filter(function(t){ try{return g.fn(t.id);}catch(e){return false;} }) : [];
      // [VF_GROUP_SEARCH_V1] キャラ名検索フィルタ
      var cq = ((document.getElementById('vf_charSearch')||{}).value||'').trim().toLowerCase();
      if (cq) chars = chars.filter(function(t){ return (t.label||'').toLowerCase().indexOf(cq)>=0 || (t.id||'').toLowerCase().indexOf(cq)>=0; });
      var csel = document.getElementById('vf_char');
      csel.innerHTML = chars.map(function(t){ var n=(t.outfits&&t.outfits.length)||(t.patterns&&t.patterns.length)||0; return '<option value="'+t.id+'">'+t.label+'  ['+n+'シーン]</option>'; }).join('');
      document.getElementById('vf_charCount').textContent = '('+chars.length+'体)';
      var saved = localStorage.getItem('_vf_char'); if (saved && chars.some(function(t){return t.id===saved;})) csel.value = saved;
      VF.previewOutfits();
    },
    outfitsOf: function(t){ if(!t) return []; var o=(t.outfits&&t.outfits.length)?t.outfits:(t.patterns||[]); return o.map(function(x){ return {label:x.label||x.name||'', value:x.value||x.prompt||''}; }); },
    previewOutfits: function(){
      var id = document.getElementById('vf_char').value; localStorage.setItem('_vf_char', id);
      var t = VF.allChars().find(function(x){return x.id===id;});
      var outs = VF.outfitsOf(t);
      document.getElementById('vf_to').placeholder = String(outs.length||'末');
      var el = document.getElementById('vf_outfitList');
      el.innerHTML = '<div style="font-weight:700;color:#e5e7eb;margin-bottom:6px">'+(t?t.label:'')+' — '+outs.length+'シーン</div>' + outs.map(function(o,i){ return '<div id="vf_row_'+i+'" style="padding:4px 6px;border-bottom:1px solid #1f2937;display:flex;gap:6px;align-items:flex-start"><span style="color:#6b7280;width:22px;text-align:right;flex-shrink:0">'+(i+1)+'</span><span style="flex:1;min-width:0;white-space:normal;word-break:break-word;line-height:1.3" title="'+(o.value||'').replace(/"/g,'&quot;')+'">'+(o.label||'(無題)')+'</span><span class="vf_mark" style="width:16px;color:#6b7280;flex-shrink:0">·</span></div>'; }).join('');
      try { VF.restoreMarks(); } catch(e){}
    },
    // ===== ヘッダー連携 =====
    hdrBadge: function(text, running){
      var bd=document.getElementById('vfHdrBadge'), st=document.getElementById('vfHdrStop');
      if(!bd) return;
      if (text) { bd.style.display='inline-block'; bd.textContent=text; } else { bd.style.display='none'; }
      if (st) st.style.display = running ? 'inline-block' : 'none';
      var _isErr = (text||'').indexOf('\u26a0') >= 0 || (text||'').indexOf('\u274c') >= 0 || (text||'').indexOf('ERR') >= 0;
      bd.style.background = running ? '#1e3a5f' : (_isErr ? '#7f1d1d' : '#14532d');
      bd.style.color = running ? '#93c5fd' : (_isErr ? '#fecaca' : '#86efac');
    },
    hdrResume: function(){
      var sv={}; try{ sv=JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){}
      if (!sv.char) { alert('再開できる連続作成の記録がありません'); return; }
      switchTab('verify'); VF.init();
      setTimeout(function(){
        // グループ/キャラをsavedに合わせる
        var g=(window.CHAR_GROUP_DEFS||[]).find(function(x){ try{return x.fn(sv.char);}catch(e){return false;} });
        if (g) { document.getElementById('vf_group').value=g.key; VF.fillChars(); }
        document.getElementById('vf_char').value=sv.char; VF.previewOutfits();
        if (sv.ckpt) document.getElementById('vf_ckpt').value=sv.ckpt;
        if (sv.from) document.getElementById('vf_from').value=sv.from;
        if (sv.to) document.getElementById('vf_to').value=sv.to;
        // [VF_VIDEO_COMPOSE_RESUME_FIX 2026-10-09] 自動再起動後の「続きから」が
        // 動画素材モード(_videoComposeNext)を保持していなかったため、動画素材生成中に
        // ComfyUIが落ちて自動再開すると通常の静止画モードに戻ってしまっていた。
        // 保存されたvideoComposeフラグを再開直前に復元する。
        VF._videoComposeNext = !!sv.videoCompose;
        VF.run(true);
      }, 150);
    },
    hdrRerun: function(){
      var sv={}; try{ sv=JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){}
      if (!sv.char) { alert('直前の連続作成の記録がありません'); return; }
      switchTab('verify'); VF.init();
      setTimeout(function(){
        var g=(window.CHAR_GROUP_DEFS||[]).find(function(x){ try{return x.fn(sv.char);}catch(e){return false;} });
        if (g) { document.getElementById('vf_group').value=g.key; VF.fillChars(); }
        document.getElementById('vf_char').value=sv.char; VF.previewOutfits();
        if (sv.from) document.getElementById('vf_from').value=sv.from;
        if (sv.to) document.getElementById('vf_to').value=sv.to;
        var sel=document.getElementById('vf_ckpt');
        var opts=Array.from(sel.options).filter(function(o){return o.value && !o.disabled;});
        var names=opts.map(function(o,i){return (i+1)+': '+o.text;}).join('\n');
        var cur=opts.findIndex(function(o){return o.value===sv.ckpt;});
        var ans=prompt('別プリセットで同じキャラ・範囲('+(sv.from||1)+'-'+(sv.to||'末')+')をもう1周します。\n番号を入力:\n'+names, String(cur>=0 ? ((cur+1)%opts.length)+1 : 1));
        var n=parseInt(ans||''); if(!n||!opts[n-1]) return;
        sel.value=opts[n-1].value;
        VF.run(false);
      }, 150);
    },
    hdrComfyClick: async function(btn){
      var alive = await VF.comfyAlive();
      if (alive) { VF.setComfyDot(true); return; }
      if (!confirm('ComfyUI(8188) が停止しています。再起動しますか？')) return;
      btn.textContent='🔁 起動中'; try { await fetch(API+'/api/restart-comfyui',{method:'POST',cache:'no-store'}); } catch(e){}
    },
    setComfyDot: function(alive){
      var d=document.getElementById('vfComfyDot'); if(!d) return;
      d.textContent = alive ? '🟢 CONF' : '🔴 CONF'; d.style.background = alive ? '#052e16' : '#7f1d1d'; d.style.color = alive ? '#86efac' : '#fecaca';
      d.title = alive ? 'ComfyUI(8188) 稼働中' : 'ComfyUI(8188) 停止中 — クリックで再起動';
    },
    startComfyWatch: function(){
      if (VF._watch) return;
      // VF_AUTO_RESUME_V1: ComfyUI 停止で中断(_haltedByComfy)していたら、🟢復帰を検知して自動で「⏩ 続きから」
      var tick = async function(){
        var alive = await VF.comfyAlive(); VF.setComfyDot(alive);
        if (alive && VF._haltedByComfy && !VF._running) {
          var ar = document.getElementById('vf_autoRestart'); if (ar && !ar.checked) return;
          if (!VF._resumeArmed) { VF._resumeArmed = Date.now(); VF.setStatus('🟢 ComfyUI 復帰検知 → 20秒後に自動で「⏩ 続きから」…'); return; }
          if (Date.now() - VF._resumeArmed < 20000) return;
          VF._resumeArmed = 0; VF._haltedByComfy = false;
          try { VF.setStatus('⏩ 自動再開…'); VF.hdrResume(); } catch(e){ console.warn('[VF_AUTO_RESUME]', e); }
        } else if (!alive) { VF._resumeArmed = 0; VF._armedAny = 0; }
        // AUTO_RESUME_ANY_V1: 理由を問わず「実行中でない＆手動停止でない＆未完了が残っている＆Comfy生存」なら自動で続きから再開
        if (alive && !VF._running && !VF._userStopped && !VF._haltedByComfy) {
          try {
            var sv = {}; try{ sv = JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){ sv = {}; }
            if (sv && sv.char && sv.results) {
              var _from = parseInt(sv.from||1,10), _to = parseInt(sv.to||0,10);
              var _total = (_to>0 ? (_to-_from+1) : (sv.results.length||0));
              var _doneOk = (sv.results||[]).filter(function(r){ return r && r.ok && r.image_path; }).length;
              if (_total>0 && _doneOk < _total) {
                if (!VF._armedAny) { VF._armedAny = Date.now(); VF.setStatus('🔁 未完了 '+(_total-_doneOk)+'/'+_total+' を検知 → 20秒後に自動再開…'); }
                else if (Date.now() - VF._armedAny >= 20000) {
                  VF._armedAny = 0;
                  try { VF.setStatus('🔁 自動再開（続きから）…'); VF.hdrResume(); } catch(e){ console.warn('[AUTO_RESUME_ANY]', e); }
                }
              } else { VF._armedAny = 0; }
            }
          } catch(e){}
        } else { VF._armedAny = 0; }
        // [VF_HANG_WATCHDOG_V1 2026-10-06] ユーザー要望: 「ログ監視してまったく動きがなかったら
        // ■停止 → ⏩続きから を実施して欲しい」。既存のAUTO_RESUME_ANY_V1は
        // VF._running===falseの場合のみ発火するため、生成処理自体がハングして
        // VF._running===trueのまま固まった(ログが全く増えない)ケースは救済されなかった。
        // [VF_HANG_WATCHDOG_FIX_V1 2026-10-06] ユーザー報告「直らない」: 当初window._opLogLastTs
        // (全ログ共通の最終更新時刻)を基準にしていたが、「同期補正」ログが無関係に5秒おきに
        // 発火し続けるため、本当に生成が進んでいなくても_opLogLastTsが常に更新され、ハング
        // 判定が一度も発火しなかった。判定基準を「VF.setStatusに渡された進捗テキスト自体が
        // 変化したか」に変更する(hookVFのラップでVF._lastStatusText/VF._lastStatusTs を更新)。
        // ここでは「連続生成が実行中(VF._running)かつ、進捗テキストの最終更新から90秒以上
        // 経過している」場合にハングと判定し、VF.stop()で強制停止→自動で
        // VF.hdrResume()(⏩続きから)を呼ぶ。手動停止(_userStopped)扱いにしないよう
        // stop()直後にフラグを明示的にリセットする。
        // [VF_HANG_WATCHDOG_SINGLE_GUARD_V1 2026-10-09] VF.runOne(単発1シーン生成)実行中は
        // このウォッチドッグを無効化する(詳細はVF.runOne定義側のコメント参照)。
        // [VF_HANG_WATCHDOG_THRESHOLD_FIX_V1 2026-10-09] 根本原因: 閾値90秒が、
        // このGPU(8GB VRAM)+Krea2系checkpointでの実際の1枚あたり生成時間
        // (実測89.9s/90.2s/95.8s/104.1s等)とほぼ同じだったため、生成が正常に
        // 進行中でも「ハング」と誤判定され、VF.stop()でComfyUI処理を強制中断
        // → VF.hdrResume()で先頭outfitから再開、という誤動作が繰り返されていた。
        // 中断されたoutfitは一度も成功完了しないため、同じoutfit(例:107番)だけを
        // 永遠に作り直し続ける無限ループになっていた(ユーザー報告の実体)。
        // 閾値を実測生成時間に十分な余裕を持つ240秒に延長する。
        if (alive && VF._running && !VF._singleRunActive) {
          var _lastLog = VF._lastStatusTs || window._opLogLastTs || 0;
          var _idleMs = Date.now() - _lastLog;
          // [VF_HANG_FALSE_POSITIVE_FIX_V1 2026-10-14] ユーザー報告:「ハング扱いされるのも
          // 意味不明」。実際のログはUltimateSDUpscale等の後処理(タイル分割アップスケール)で
          // 絶え間なく流れていたが、進捗テキストの「X/Y」部分(VF._lastStatusCore)が
          // パネル完了まで変化しないため_lastStatusTsが更新されず、240秒閾値を超えて
          // 誤ってハングと判定されていた(実測321秒で誤検知)。ComfyUI本体の/queueが
          // 実際にジョブを処理中(queue_running非空)であれば、本当にハングしている
          // 可能性は低いため誤検知を避け、ウォッチドッグの作動を見送る。
          var _reallyIdle = true;
          try {
            var _qResp = await fetch(API + '/queue', {cache:'no-store'});
            var _qJson = await _qResp.json();
            if (_qJson && Array.isArray(_qJson.queue_running) && _qJson.queue_running.length > 0) _reallyIdle = false;
          } catch(_qErr) { /* 取得失敗時は従来通りタイマーのみで判定 */ }
          if (_lastLog > 0 && _idleMs > 240000 && _reallyIdle) {
            // [VF_HANG_RESPONSE_SPEEDUP_V1 2026-10-14] ユーザー報告:「検知してから実際に
            // 停止して続きから試みるのが遅すぎ。疑いの時点ですぐ停止続きしてほしい」。
            // 旧実装は「疑い」メッセージ表示後さらに5秒armed待ち+停止後4秒待ってから
            // resumeという合計9秒の無駄な遅延があった(二重確認は誤検知防止の意図だったが、
            // 既に_reallyIdleチェックでComfyUI本体のqueue_runningを確認済みのため、
            // この追加待機は冗長)。検知した時点で即座に停止・再開する。
            if (!VF._hangArmed) {
              VF._hangArmed = Date.now();
              VF.setStatus('⚠️ ログ無動作 ' + Math.round(_idleMs/1000) + '秒検知 → ハング確定、即座に停止して続きから再開します…');
              try {
                console.warn('[VF_HANG_WATCHDOG] idle=' + _idleMs + 'ms → force stop & resume (immediate)');
                VF.stop();
                VF._running = false;
                VF._userStopped = false; VF._haltedByComfy = false; VF._stop = false;
                VF.setStatus('⏩ ハング復旧: 続きから再開…');
                try { VF.hdrResume(); } catch(e2){ console.warn('[VF_HANG_WATCHDOG] resume failed', e2); }
              } catch(e){ console.warn('[VF_HANG_WATCHDOG]', e); }
            }
          } else { VF._hangArmed = 0; }
        } else { VF._hangArmed = 0; }
        // [COMFY_QUEUE_HANG_WATCHDOG_V1 2026-10-06] ユーザー報告(05:51): 上記
        // VF_HANG_WATCHDOG_V1は「VF._running(連続生成ループ中)」限定の判定だったため、
        // ▶生成ボタン等の単発generateSinglePanel呼び出し中は一切発火せず、「同期補正」
        // ログ(5秒おきの無関係な定期処理、forceResyncAllPanels)がwindow._opLogLastTsを
        // 絶えず更新し続けるため、VF._running===falseの間はハング判定条件自体に
        // 到達しなかった(根本原因)。VF._running/VF._lastStatusTsに依存せず、
        // ComfyUI本体の/queueを直接見て「queue_runningの同一prompt_idがcreate_timeから
        // 90秒以上経過しても変わらない」場合に本当のハングと判定し、/api/stopで
        // ComfyUIのキューとexecutionを強制キャンセルする(次のポーリングでComfyUI側が
        // 次のジョブを拾う→本体の各リトライ/自動再開ロジックに委ねる)。
        if (alive) {
          try {
            var _qr = await (await fetch('http://127.0.0.1:8188/queue', {cache:'no-store'})).json();
            var _running0 = (_qr && _qr.queue_running && _qr.queue_running[0]) || null;
            var _curPid = _running0 ? _running0[1] : null;
            var _curCreateTime = (_running0 && _running0[3] && _running0[3].create_time) || null;
            // [VIDEO_HANG_THRESHOLD_FIX_V1 2026-10-06] ユーザー報告:「動画生成は時間
            // かかるのにハング扱いされる」。従来は画像生成(通常数十秒)も動画生成
            // (WAN22/リップシンク等、数分〜十数分かかるのが正常)も同じ90秒の閾値で
            // ハング判定していたため、正常に進行中の動画生成が強制キャンセルされていた。
            // prompt(ノード定義)に動画系ワークフローの特徴的なnode/ファイル名が
            // 含まれるかを見て、動画ジョブの場合は閾値を大幅に延長する。
            var _cqIsVideo = false;
            try {
              var _promptDump = JSON.stringify((_running0 && _running0[2]) || {}).toLowerCase();
              _cqIsVideo = /wan22|wanvideo|videocombine|video_combine|lipsync|wan_video|vhs_|animatediff|svd_img2vid/.test(_promptDump);
            } catch(_cqvErr) {}
            // [VF_HANG_WATCHDOG_THRESHOLD_FIX_V1 2026-10-09] 画像側も120秒は実測生成時間
            // (89.9s~104.1s)に対して余裕がなく誤爆の一因だったため240秒に延長。
            var _cqThreshold = _cqIsVideo ? 900000 : 240000;  // 動画=15分、画像=240秒
            if (_curPid && _curCreateTime) {
              if (VF._cqPid !== _curPid) { VF._cqPid = _curPid; VF._cqCreateTime = _curCreateTime; VF._cqArmed = 0; }
              var _runMs = Date.now() - _curCreateTime;
              if (_runMs > _cqThreshold) {
                if (!VF._cqArmed) {
                  VF._cqArmed = Date.now();
                  console.warn('[COMFY_QUEUE_HANG_WATCHDOG] prompt_id=' + _curPid + ' running=' + Math.round(_runMs/1000) + 's → ハング疑い');
                  if (typeof window._opLog === 'function') window._opLog('warn', '⚠️ [COMFY_QUEUE_HANG_WATCHDOG] ComfyUIが同一ジョブを' + Math.round(_runMs/1000) + '秒以上処理中 → ハング疑いでキューを強制キャンセルします');
                } else if (Date.now() - VF._cqArmed >= 5000) {
                  VF._cqArmed = 0; VF._cqPid = null;
                  try {
                    await fetch(API + '/api/stop', {method:'POST'}).catch(function(){});
                    if (typeof window._opLog === 'function') window._opLog('warn', '✅ [COMFY_QUEUE_HANG_WATCHDOG] キューを強制キャンセルしました(次のジョブから再開されます)');
                  } catch(_cqe) { console.warn('[COMFY_QUEUE_HANG_WATCHDOG] stop failed', _cqe); }
                }
              } else { VF._cqArmed = 0; }
            } else { VF._cqPid = null; VF._cqArmed = 0; }
          } catch(_cqErr) { /* ComfyUI未応答時は何もしない(他の監視に委ねる) */ }
        } else { VF._cqPid = null; VF._cqArmed = 0; }
      };
      tick(); VF._watch = setInterval(tick, 10000);
    },
    openOutput: async function(){
      try { var r=await fetch(API+'/api/open-folder',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:'C:\\AI\\ComfyUI\\output'})}); var d=await r.json(); if(!d.ok) alert('開けませんでした: '+(d.error||'')); } catch(e){ alert('開けませんでした: '+e.message); }
    },
    cleanupTmp: async function(btn){
      try {
        var r=await fetch(API+'/api/output/cleanup-tmp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({dry_run:true})}); var d=await r.json();
        if (!d.count) { alert('一時ファイルはありません'); return; }
        if (!confirm('一時ファイル '+d.count+' 件 ('+(d.bytes/1048576).toFixed(1)+' MB) をゴミ箱へ移動します。よろしいですか？')) return;
        r=await fetch(API+'/api/output/cleanup-tmp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({})}); d=await r.json();
        alert('掃除完了: '+d.count+' 件 → '+(d.via==='recycle_bin'?'ゴミ箱':'output/_trash')+(d.errors&&d.errors.length?'\nエラー: '+d.errors.join('\n'):''));
      } catch(e){ alert('失敗: '+e.message); }
    },
    waitLock: async function(maxSec){
      // 他クライアント(ベンチ含む)がロック保持中なら空くまで待つ。本番はベンチより優先されるので通常60秒以内に空く
      var t0 = Date.now(); maxSec = maxSec || 60;
      while (!VF._stop && (Date.now() - t0) / 1000 < maxSec) {
        try {
          var st = await (await fetch((window.API_BASE||location.origin)+'/api/gen-lock?waiting=1', {cache:'no-store'})).json();  // waiting=1: 本番が待っている＝ベンチ抑止を継続
          if (!st.busy || st.mine) return true;
          VF.setStatus((st.owner_is_bench ? '⏳ ベンチの1枚が終わるのを待機中（終われば本番優先で停止します）… ' : '⏳ 他タブの生成完了を待機中… ') + Math.round((Date.now()-t0)/1000) + 's');
        } catch(e) { return true; }
        await new Promise(function(r){ setTimeout(r, 3000); });
      }
      return !VF._stop;
    },
    // COMFY_ALIVE_DIRECT_V1 (2026-09-25): API(3002)が落ちている/再起動中でも ComfyUI(8188) を直接見る。
    // 旧実装は API 不通 = ComfyUI 停止 と誤判定し、健全な ComfyUI を /api/restart-comfyui で殺していた（19:57 の再起動連鎖）
    comfyAlive: async function(){
      try { var r = await fetch(API+'/api/status', {cache:'no-store'}); var d = await r.json(); if (d && d.comfyui === 'running') return true; } catch(e){}
      try { var q = await fetch('http://127.0.0.1:8188/prompt', {cache:'no-store'}); if (q.ok) return true; } catch(e){}
      return false;
    },
    // API_WAIT_V1: API(3002) が watchdog 再起動中なら最大 90 秒待つ（生成ループを止めない）
    apiAlive: async function(){ try { var r = await fetch(API+'/health', {cache:'no-store'}); return r.ok; } catch(e){ return false; } },
    waitApi: async function(maxSec){
      maxSec = maxSec || 90;
      for (var w=0; w<maxSec; w++) { if (await VF.apiAlive()) return true; if (VF._stop) return false; if (w===0 || w%5===0) VF.setStatus('⏳ APIサーバー再起動待ち… '+w+'s'); await new Promise(function(r){setTimeout(r,1000);}); }
      return false;
    },
    ensureComfy: async function(){
      if (!(await VF.apiAlive())) { if (!(await VF.waitApi(30))) { VF.setStatus('❌ APIサーバー(3002)が90秒以内に復帰しませんでした'); return false; } await new Promise(function(r){setTimeout(r,3000);}); }  // API_WAIT_V1
      if (await VF.comfyAlive()) return true;
      if (!document.getElementById('vf_autoRestart').checked) { VF.setStatus('❌ ComfyUI(8188) が停止しています。「⚙️ CONF再起動」を押してください'); return false; }
      VF.setStatus('⚠️ ComfyUI が停止 → 自動再起動中…');
      try { await fetch(API+'/api/restart-comfyui', {method:'POST', cache:'no-store'}); } catch(e){}
      for (var w=0; w<45; w++) { // [COMFY_RESTART_WAIT_V1 2026-10-15] 90s->45s // 最大90秒待つ
        await new Promise(function(r){setTimeout(r,1000);});
        if (VF._stop) return false;
        if (await VF.comfyAlive()) { VF.setStatus('✅ ComfyUI 復帰。10秒待機してから再開…'); await new Promise(function(r){setTimeout(r,10000);}); return true; }
        if (w%5===0) VF.setStatus('⚠️ ComfyUI 再起動待ち… '+w+'s');
      }
      VF.setStatus('❌ ComfyUI が90秒以内に復帰しませんでした'); return false;
    },
    setStatus: function(s, pct){
      document.getElementById('vf_status').textContent = s; if(pct!=null) document.getElementById('vf_bar').style.width = pct+'%';
      // [VF_HANG_WATCHDOG_FIX_V1 2026-10-06] 進捗テキストの「X/Y」部分(時間・ETA等の
      // 付随情報を除いた本体)が前回と変わったかどうかでVF._lastStatusTsを更新する。
      // ⏱ 残り約...秒のような末尾の時刻情報だけ変わるケースは「進んでいない」と見なす。
      try {
        var _coreMatch = /(\d+)\s*\/\s*(\d+)/.exec(s||'');
        var _core = _coreMatch ? _coreMatch[0] : (s||'');
        if (_core !== VF._lastStatusCore) { VF._lastStatusCore = _core; VF._lastStatusTs = Date.now(); }
        else if (!VF._lastStatusTs) { VF._lastStatusTs = Date.now(); }
      } catch(e){}
      // [VF_HDR_PROGRESS_BAR_FIX_V1 2026-10-06] pctが渡らない呼び出しでも直前値を保持して
      // 常時表示側のバーに反映する(style.width文字列の読み戻しは信頼できないため数値で保持)。
      if (pct!=null) VF._lastPct = pct;
      try {
        var hb=document.getElementById('vfHdrProgBar'), hw=document.getElementById('vfHdrProgressWrap');
        if (hb) hb.style.width = (VF._lastPct!=null ? VF._lastPct : 0) + '%';
        if (hw) hw.style.display = (VF._running && s) ? 'inline-block' : 'none';
      } catch(e){}
      VF.hdrBadge(s, VF._running);
    },
    // [VF_VIDEO_COMPOSE_V1 2026-10-09 / V2 2026-10-09 汎用化] 動画素材(i2v)生成用に構図タグを差し込む。
    // 旧版は「男性主体の性行為キーワードがある時だけ」固定の1パターンを注入していたため、
    // (1)医療/ピアス施術等の非性行為シーンには一切効かず、ユーザー報告の「毎回同じような
    //    股間クローズアップ構図で動いて見えない」問題を放置していた
    // (2)性行為シーンも常に同一パターンのため、連続生成すると絵面が似通い「動画にしやすい
    //    バリエーション」になっていなかった
    // → 汎用化: 全シーンに対して「i2vで動きが出やすい構図」を適用し、かつ複数パターンを
    //   outfit indexでローテーションしてバリエーションを持たせる。
    // [VF_VIDEO_COMPOSE_ACT_KWS_EXPAND_V1 2026-10-09] ユーザー指摘:「動画素材生成は
    // ピストンとか性行為になりやすい構図にするものだけど、ちゃんと核心タグ・核心構図に
    // なっているか確認して」。検証した結果、fellatio/creampie/deepthroat/facial/
    // bukkake等、多数の性行為シーンがキーワード不足で検出漏れし、一般向け構図
    // (GENERIC)のまま動画化されていた(腰を可視化するACT構図が適用されていなかった)。
    // api_server_3001.py側の_CORE_ACTION_EN_MAP(POSE_CTX_INJECTと同じカテゴリ語彙)を
    // 流用し、主要な性行為カテゴリを網羅する形に拡充。
    _VIDEO_ACT_KWS: ['doggy','missionary','mating press','mating_press','thrusting','anal','paizuri',
                      'cowgirl','piston','sex with','intercourse','penetration','vaginal sex','from behind',
                      'reverse cowgirl','standing sex','fellatio','blowjob','blow job','penis in mouth',
                      'oral sex','deepthroat','creampie','internal ejaculation','cum inside','facial',
                      'cum on face','bukkake','cumshot','sixty-nine','sixtynine','69 position',
                      'fingering','finger penetration','handjob','hand job','footjob','foot job',
                      'titjob','tit fuck','breast sex','intercrural','thigh sex','scissoring','tribbing',
                      'carried sex','held up by hands','connected genitals','penis inside vagina',
                      'penis deep in throat','penis in throat','riding penis','hips moving wildly',
                      'hips bouncing','straddling','pov male'],
    // 男性主体の性行為シーン用バリエーション（腰・骨盤がフレーム内に残る構図を複数用意）
    _VIDEO_COMPOSE_VARIANTS_ACT: [
      '(three-quarter side view:1.6),(camera angle from the side:1.5),(male hips and thighs fully visible in frame:1.7),(not directly overhead:1.4),(not fully frontal vertical angle:1.3),(pelvis not obscured:1.4),(visible hip joint motion:1.3)',
      '(side profile view:1.6),(camera at waist height:1.5),(male hips and thighs fully visible in frame:1.7),(not directly overhead:1.4),(low angle from the side:1.3),(pelvis not obscured:1.4),(visible hip joint motion:1.3)',
      '(low angle three-quarter view:1.6),(camera slightly below hip level:1.5),(male hips and thighs fully visible in frame:1.7),(not directly overhead:1.4),(not fully frontal vertical angle:1.3),(pelvis not obscured:1.4),(dynamic motion blur on hips:1.2)'
    ],
    // [VF_VIDEO_COMPOSE_GENERIC_V1 2026-10-09] 性行為タグが無い一般シーン(医療/ピアス施術/
    // 日常/泣き崩れ等)向け。i2vで動きが出やすいよう、真上固定/真正面固定を避け、体の輪郭・
    // 手足の関節が見える角度を複数パターン用意してローテーションする。
    _VIDEO_COMPOSE_VARIANTS_GENERIC: [
      '(three-quarter angle view:1.5),(camera slightly to the side:1.4),(not directly overhead:1.3),(not fully frontal flat angle:1.2),(body contour visible:1.2),(natural joint motion:1.2)',
      '(side view with slight elevation:1.5),(camera at chest height:1.4),(not directly overhead:1.3),(limbs visible in frame:1.3),(natural joint motion:1.2)',
      '(dynamic three-quarter view:1.5),(camera angled from below:1.4),(not fully frontal flat angle:1.2),(full body motion visible:1.3),(natural joint motion:1.2)'
    ],
    videoComposePrompt: function(promptText, variantIdx){
      var low = (promptText||'').toLowerCase();
      if (low.indexOf('three-quarter') >= 0 || low.indexOf('side view') >= 0) return promptText; // 既に構図指定済みなら二重注入しない
      var hit = VF._VIDEO_ACT_KWS.some(function(k){ return low.indexOf(k)>=0; });
      var variants = hit ? VF._VIDEO_COMPOSE_VARIANTS_ACT : VF._VIDEO_COMPOSE_VARIANTS_GENERIC;
      var idx = ((variantIdx||0) % variants.length + variants.length) % variants.length;
      var tag = variants[idx];
      return tag + ',' + (promptText||'');
    },
    run: async function(resume){
      if (VF._running) return;
      // [VF_RUN_GENERATION_TOKEN_V1 2026-10-14] ユーザー報告:「同じ画像が何枚も
      // できて先に進まない」「キューが何個も入る」。根本原因: ハング誤検知(または
      // 真のハング)でVF.stop()→VF._running=falseリセット→4秒後に新しいVF.run()
      // ループを起動する復旧処理が、古いループ(await generateSinglePanel等で
      // 本当にブロックしているだけで、ComfyUI側は実際には処理を続けている場合)を
      // 一切止めないまま新しいループと並走させていた。両方のループが同じ/次の
      // シーンへ画像生成リクエストを送るため、同一シーンの重複生成・ComfyUIへの
      // キュー二重投入が発生していた。世代トークンを導入し、新しいrun()が始まる
      // 際に世代番号をインクリメント。各ループ反復で自分の世代が最新でなくなって
      // いたら(=別の新しいrun()が開始された)即座に処理を中断する。
      var _myGen = (VF._runGen = (VF._runGen||0) + 1);
      var id = document.getElementById('vf_char').value;
      var t = VF.allChars().find(function(x){return x.id===id;});
      var outs = VF.outfitsOf(t);
      if (!t || !outs.length) { alert('このキャラにはOUTFIT/シーンがありません'); return; }
      var from = Math.max(1, parseInt(document.getElementById('vf_from').value||'1'));
      var to = parseInt(document.getElementById('vf_to').value||'') || outs.length; to = Math.min(to, outs.length);
      var ckpt = document.getElementById('vf_ckpt').value; localStorage.setItem('_vf_preset', ckpt);  // ckpt = プリセットkey

      // 検証用 pages を構築: 1outfit = 1ページ1コマ
      // [VF_VIDEO_COMPOSE_V1 2026-10-09] VF._videoComposeNext が立っている場合、
      // i2v（動画素材）用に、男性主体の性行為シーンの構図タグを差し込む。
      // 理由: WAN2.2 i2v は最初のフレームの姿勢から「動かす対象（腰・骨盤）が
      // 画面に写っていて、真上/真正面ではなく斜め〜横から見える」構図でないと
      // ピストン運動が再現されにくい（画像解析で確認済み）。
      var _vfVideoMode = !!VF._videoComposeNext; VF._videoComposeNext = false;
      var pages = [];
      for (var i=from-1; i<to; i++) {
        var o = outs[i];
        var _outfitVal = o.value||'';
        if (_vfVideoMode) _outfitVal = VF.videoComposePrompt(_outfitVal, i);
        pages.push({ background_note:'', page_title:'VERIFY '+(i+1), panels:[{
          speaker:'character1', dialogue:o.label||'', text:o.label||'', prompt:'', base_prompt:'', em_tags:'',
          char_template_id: t.id, outfit_label:o.label||'', outfit_prompt:_outfitVal, current_outfit:o.label||'',
          image_path:null, seed:-1, _verify:true, _vf_idx:i, _vf_video_mode:_vfVideoMode
        }]});
      }
      // 既存 _pagesData をバックアップして差し替え（PDF/表示は既存ロジックを流用）
      if (!window._vfBackupPages && !localStorage.getItem('_vfBackupPages')) { try { window._vfBackupPages = JSON.stringify(window._pagesData||[]); localStorage.setItem('_vfBackupPages', window._vfBackupPages); } catch(e){} }
      VF._cleared=false;
      window._pagesData = pages; localStorage.setItem('_pagesData', JSON.stringify(pages)); localStorage.setItem('pagesData', JSON.stringify(pages));
      try { renderPageList(pages); } catch(e){}
      // プリセット適用: コマの 📸/🎨 ボタン(__switchPreset)と同じ動作を全コマに
      if (ckpt && typeof __switchPreset === 'function') {
        for (var q=0; q<pages.length; q++) { try { __switchPreset(ckpt, q, 0); } catch(e){ console.warn('[VERIFY] preset apply fail', e); } }
        try { hideLog(); } catch(e){}
      }
      // VF_MANUAL_PARAMS_V1: 手動指定を全コマへ（空欄はプリセット既定のまま）
      try { VF.applyParamsTo(pages); } catch(e){ console.warn('[VF params]', e); }

      var prev = {};
      if (resume) { try { var sv0 = JSON.parse(localStorage.getItem('_vf_results')||'{}'); if (sv0.char===t.id) (sv0.results||[]).forEach(function(r){ if(r.ok) prev[r.idx]=r; }); } catch(e){} }
      VF._running=true; VF._stop=false; VF._userStopped=false; /*AUTO_RESUME_ANY_V1*/ VF._results=Object.keys(prev).map(function(k){return prev[k];}).sort(function(a,b){return a.idx-b.idx;});
      // 本番優先ハートビート: 実行中は20秒ごとに ?waiting=1 を送り、ベンチが再開しないようにする
      if (VF._hb) clearInterval(VF._hb);
      VF._hb = setInterval(function(){ if (!VF._running) { clearInterval(VF._hb); VF._hb=null; return; } fetch((window.API_BASE||location.origin)+'/api/gen-lock?waiting=1', {cache:'no-store'}).catch(function(){}); }, 20000); if(!resume) localStorage.removeItem('_vf_results'); VF.renderGallery();
      // 既に成功済みのコマは image_path を復元して表示
      pages.forEach(function(pg){ var pn=pg&&pg.panels&&pg.panels[0]; if (pn&&prev[pn._vf_idx]) { pn.image_path = prev[pn._vf_idx].image_path; var rw=document.getElementById('vf_row_'+pn._vf_idx); if(rw) rw.querySelector('.vf_mark').textContent='✅'; } }); // [VF_PREV_GUARD_V1]
      if (!await VF.ensureComfy()) { VF._running=false; VF._haltedByComfy=true; /*VF_AUTO_RESUME_V1*/ return; }
      var rb=document.getElementById('vf_runBtn'), sb=document.getElementById('vf_stopBtn'); rb.disabled=true; rb.style.opacity=.5; sb.disabled=false; sb.style.opacity=1;
      var total = to-from+1, done=0, t0=Date.now();
      for (var p=0; p<pages.length; p++) {
        if (VF._stop) break;
        // [VF_RUN_GENERATION_TOKEN_V1 2026-10-14] 自分より新しいrun()が開始されていたら
        // (ハング復旧等で新ループが走り出した)、古いループはここで即座に離脱する。
        if (VF._runGen !== _myGen) { console.warn('[VF_RUN_GENERATION_TOKEN] stale loop(gen='+_myGen+' current='+VF._runGen+') -> abort'); break; }
        if (!pages[p] || !pages[p].panels || !pages[p].panels[0]) { done++; continue; } // [VF_OI_GUARD_V1 2026-10-15]
        var oi = pages[p].panels[0]._vf_idx;
        var row = document.getElementById('vf_row_'+oi); if(row){ row.style.background='#1e3a5f'; row.querySelector('.vf_mark').textContent='⏳'; }
        VF.setStatus('生成中 '+(done+1)+'/'+total+' : '+(outs[oi].label||''), Math.round(done/total*100)); VF._panelStart = Date.now();
        if (prev[oi]) { row = document.getElementById('vf_row_'+oi) || row; if(row){ row.style.background=''; var _m0=row.querySelector('.vf_mark'); if(_m0) _m0.textContent='✅'; } done++; continue; }  // 続きから: 成功済みはスキップ
        var t1=Date.now();
        var img = '', lastErr = '';
        for (var attempt=0; attempt<4 && !VF._stop; attempt++) {  // [VF_RETRY_4_V1 2026-10-15] 6->4
          try {
            if (attempt>0) { VF.setStatus('再試行 '+(attempt)+' '+(done+1)+'/'+total+' : '+(outs[oi].label||'')+' ('+Math.round((Date.now()-t1)/1000)+'s)'); if (!await VF.ensureComfy()) break; }
            if (!await VF.waitLock(60)) break;   // ロック待ち（ベンチ/他タブ）
            if (!window._pagesData[p] || !window._pagesData[p].panels || !window._pagesData[p].panels[0]) { lastErr='pagesData missing'; break; } // [VF_PAGES_GUARD_V1 2026-10-15]
            var pn = window._pagesData[p].panels[0]; pn.image_path = null; pn._img_latest = null;
            // [VF_OUTFIT_FORCE_SYNC_V1 2026-10-21] リトライ中や_pagesData再構築後に
            // outfit_promptが別コマのキャッシュ値に戻ってしまう問題を防ぐため、
            // generateSinglePanel呼び出し直前に毎回outs[oi]の値で強制上書きする。
            if (outs[oi]) { pn.outfit_prompt = outs[oi].value || ''; pn.outfit_label = outs[oi].label || ''; pn.current_outfit = outs[oi].label || ''; }
            // [VF_MANUAL_SELECTED_RESET_FIX 2026-10-13] generateSinglePanelは
            // _img_manual_selected===trueのパネルに対してimage_pathを一切更新しない
            // ガードを持つため、このフラグが残っていると「生成は正常完了している
            // のにpn.image_pathが永遠に埋まらず、VFの待機ループがタイムアウト→
            // 失敗扱いで同じリクエストを再送信し続ける」原因になっていた
            // (#98/#99: 生成完了してるのに同期されず同じリクエストが何度も飛ぶ)。
            pn._img_manual_selected = false;
            delete window['_gen_lock_'+p+'_0'];
            window.__genLockBusy = null;
            await generateSinglePanel(p, 0);
            // [VF_RUN_GENERATION_TOKEN_V1 2026-10-14] generateSinglePanel完了後、自分が
            // 既に古い世代になっていたら(待機中にハング復旧で新ループが始まっていた)、
            // 結果の反映・次のリトライを行わずループごと離脱する(重複生成防止)。
            if (VF._runGen !== _myGen) { console.warn('[VF_RUN_GENERATION_TOKEN] stale after generate(gen='+_myGen+' current='+VF._runGen+') -> abort'); break; }
            if (window.__genLockBusy) { lastErr = '409 busy'; window.__genLockBusy = null; await new Promise(function(r){setTimeout(r,2000);}); continue; }  // [VF_BUSY_WAIT_V1] 409 → 待って再試行
            // [VF_PAN_REREF_V1 2026-10-15] generateSinglePanel後にpnの参照を取り直す(renderPageListで_pagesDataが差し替わるバグ対策)
            pn = (window._pagesData[p] && window._pagesData[p].panels && window._pagesData[p].panels.length > 0 && window._pagesData[p].panels[0]) || pn; // [VF_PAN_REREF_GUARD_V1]
            var w=0; while (!pn.image_path && w<800 && !VF._stop && VF._runGen===_myGen) { await new Promise(function(r){setTimeout(r,150);}); w++; } // [VF_IMGWAIT_TIMEOUT_V1 2026-10-15] 300s->120s // [FAST_SYNC_V1 2026-10-14] 500ms→150ms
            img = pn.image_path||'';
            // [VF_OUTFIT_VERIFY_V1 2026-09-28] リクエスト重複/競合により、別outfitの
            // 画像がこのpn.image_pathに紛れ込むケースがあった(サーバー側の生成ロックが
            // client_id単位で再入可能なため、同一ブラウザからの並行/重複送信を防げない)。
            // 生成完了後、実際にサーバー側が処理したoutfit_promptを問い合わせて
            // 期待値と一致するか検証し、不一致ならこの結果は捨てて再試行する。
            if (img) {
              try {
                // [VF_OUTFIT_VERIFY_IMGPATH_FIX_V1 2026-10-13] 旧実装はプロンプト文字列の
                // 前方60文字の完全一致で検証していたが、サーバー側は年齢タグ挿入・衣装マージ・
                // 構図タグ付与などの前処理でプロンプト文字列を大きく書き換えるため、実際には
                // 正しいoutfitで正常生成できていても高頻度で「不一致」と誤判定していた
                // (#98/#99: 生成完了してるのに同期されず同じリクエストが何回も飛ぶ、
                // 16/185で止まり続ける 等の根本原因)。サーバー側キャッシュが記録する
                // 実際の画像パス(_image_path)がこのimgと一致するかで検証する方が確実。
                var _vfCheck = await (await fetch(API+'/api/panel-prompt?page='+oi+'&panel=0', {cache:'no-store'})).json();
                var _actualImgPath = _vfCheck && (_vfCheck._image_path || _vfCheck._output_url || '');
                if (_actualImgPath && img && !_actualImgPath.includes(img.split('/').pop()) && !img.includes((_actualImgPath.split('/').pop()||'\u0000'))) {
                  console.warn('[VF_OUTFIT_VERIFY] image mismatch! expected_contains='+img+' actual='+_actualImgPath+' -> retry');
                  lastErr = '画像不一致(競合検知)'; img = ''; pn.image_path = null;
                  await new Promise(function(r){setTimeout(r,2000);});
                  continue;
                }
              } catch(_vfe) { console.warn('[VF_OUTFIT_VERIFY] check skip', _vfe); }
            }
            if (img) break;
            lastErr = '画像なし';
            if (!(await VF.comfyAlive())) lastErr = 'ComfyUI停止';
          } catch(e) { console.error('[VERIFY] fail', e); lastErr = String(e&&e.message||e); }
        }
        VF._results = VF._results.filter(function(r){return r.idx!==oi;});
        // [VF_PANEL_PROMPT_KEY_FIX 2026-09-28] page_idx に一時ループ変数pを使うと、
        // VF検証はp=0を毎outfitで再利用するため /api/panel-prompt?page=0&panel=0 の
        // キャッシュが直後の別outfitに即上書きされ、AIコピーボタンで別コマの
        // プロンプト情報が表示される実害があった。oi(恒久的なoutfit連番)をpage_idxに使う。
        VF._results.push({idx:oi, label:outs[oi].label, image_path:img, sec:((Date.now()-t1)/1000).toFixed(1), ok:!!img, err: img?'':lastErr, page_idx:oi, panel_idx:0});
        VF._results.sort(function(a,b){return a.idx-b.idx;});

        // [VF_MARK_SYNC_FIX_V1 2026-10-14] ユーザー報告:「進捗バーと⌛で整合性が取れてない」。
        // 生成中(リトライ含め数十秒〜数分)の間にrenderGallery/previewOutfits等でリストDOMが
        // 再構築されると、ループ先頭で取得した古いrow変数はDOMツリーから切り離され、
        // 完了時にそこへ✅/❌を書いても画面に反映されず⌛表示のまま取り残されていた。
        // 完了直前に行を再取得してから更新する。
        row = document.getElementById('vf_row_'+oi) || row;
        if(row){ row.style.background=''; var _m=row.querySelector('.vf_mark'); if(_m) _m.textContent = img?'✅':'❌'; }
        if (!img && !VF._stop && !(await VF.comfyAlive())) {
          // 落ちたままなら次へ行く前に復帰を試す。無理なら中断（続きからで再開可）
          if (!await VF.ensureComfy()) { VF._stop = true; VF._haltedByComfy=true; /*VF_AUTO_RESUME_V1*/ VF.setStatus('❌ ComfyUI 停止のため中断。復帰後「⏩ 続きから」で再開できます'); }
        }
        done++; if (VF._cleared) break; VF.renderGallery();
        // [VF_MARK_SYNC_FIX_V1 2026-10-14] 進捗バー(done/total)と左リストの⌛/✅表示がズレる
        // 問題の追加保険: 毎ループ完了直後に、これまでの全VF._resultsを根拠に左リスト全行の
        // マークを強制的に再同期する(DOM再構築で取り残された古い⌛表示を一掃)。
        try { VF._results.forEach(function(r){ var _rw=document.getElementById('vf_row_'+r.idx); if(_rw){ var _rm=_rw.querySelector('.vf_mark'); if(_rm) _rm.textContent = r.ok?'✅':'❌'; _rw.style.background=''; } }); } catch(_e) {}
        localStorage.setItem('_vf_results', JSON.stringify({char:t.id, label:t.label, ckpt:ckpt, from:from, to:to, results:VF._results, videoCompose:_vfVideoMode}));
      }
      if (VF._cleared) { VF._running=false; rb.disabled=false; rb.style.opacity=1; sb.disabled=true; sb.style.opacity=.5; return; }
      // [VF_AUTOCOMPLETE_V1 2026-10-14] ユーザー要望:「連続生成が最後まで完遂するように
      // 強化」。従来は停止ではない正常完了時でも❌が残ったまま終了表示していた。
      // ユーザーが手動停止(VF._userStopped)していない場合に限り、失敗分だけを対象に
      // 自動で1パス追加リトライする(無限ループ防止のため1回のみ・最大2周)。
      var _failedOis = (VF._results||[]).filter(function(r){return !r.ok;}).map(function(r){return r.idx;}); // [VF_RESULTS_GUARD_V1 2026-10-15]
      // [VF_AUTOCOMPLETE_V2 2026-10-15] 失敗コマを最大3パスまでリトライ (!VF._autoCompletePassのバグ修正: 1回しか発動しなかった)
      VF._autoCompletePass = (VF._autoCompletePass||0);
      if (!VF._userStopped && _failedOis.length && VF._autoCompletePass < 3) {
        VF._autoCompletePass = VF._autoCompletePass + 1;
        if (VF._autoCompletePass <= 3) {
          VF.setStatus('🔄 失敗した'+_failedOis.length+'件を自動補完リトライ中...', 100);
          console.warn('[VF_AUTOCOMPLETE_V1] retrying failed panels:', _failedOis, 'pass='+VF._autoCompletePass);
          await new Promise(function(r){setTimeout(r,2000);});
          VF._running=false; rb.disabled=false; rb.style.opacity=1; sb.disabled=true; sb.style.opacity=.5;
          if (VF._hb) { clearInterval(VF._hb); VF._hb=null; }
          if (!VF._stop) { VF._autoCompletePass = VF._autoCompletePass; return VF.run(true); }
        }
      }
      VF._autoCompletePass = 0;
      VF._running=false; rb.disabled=false; rb.style.opacity=1; sb.disabled=true; sb.style.opacity=.5;
      if (VF._hb) { clearInterval(VF._hb); VF._hb=null; }
      VF.setStatus((VF._stop?'停止(⏩続きから で再開可): ':'完了: ')+done+'/'+total+'  ('+((Date.now()-t0)/1000).toFixed(0)+'秒)  成功 '+VF._results.filter(function(r){return r.ok;}).length+' / 失敗 '+VF._results.filter(function(r){return !r.ok;}).length, 100);
    },
    stop: function(){
      VF._stop=true; VF._haltedByComfy=false; VF._userStopped=true; /*VF_AUTO_RESUME_V1 / AUTO_RESUME_ANY_V1: 手動停止は自動再開しない*/
      VF.setStatus('停止要求中… ComfyUIのリクエストも強制キャンセルします');
      // [VF_STOP_FORCE_INTERRUPT_V1 2026-10-05] ユーザー要望:「ボタン押したらCONFのリクエストも強制キャンセルして」。
      // 従来は_stopフラグのみで現在のコマ完了を待っていたが、/api/stop(ComfyUIの/queue clear + /interrupt)も
      // 同時に叩き、実行中のジョブ自体を即座に中断する。
      try {
        fetch(API + '/api/stop', {method:'POST'})
          .then(function(){ VF.setStatus('停止しました（ComfyUIリクエストも強制キャンセル済み）'); })
          .catch(function(){});
      } catch(e) {}
    },
    
recoverImg: function(imgEl, failedUrl, vfIdx){
    // [LINK_RECOVER_V1 2026-10-03] リンク切れ時にファイル名ベースで再スキャンして復元
    // [LINK_RECOVER_V2_AUTOREGEN 2026-10-14] ユーザー要望:「自動的にリンク切れを検知して
    // 再作成して、連続生成が最後まで完遂するように強化」。
    // 従来は再スキャンしても見つからなければ諦めて半透明表示のまま放置していた。
    // ここでは: ①再スキャンで見つからない ②見つかってもファイルが実際には読み込めない
    // 場合に、該当コマ(page_idx/panel_idx)をgenerateSinglePanelで自動的に再生成し、
    // 完了したら差し替える。再生成も失敗したら一定回数までリトライしてから諦める。
    if (imgEl._recovering) return;
    imgEl._recovering = true;
    imgEl.style.opacity = '0.3';
    imgEl.title = '🔄 リンク切れ検知→復旧中...';
    var fname = failedUrl.split('/').pop().split('?')[0];
    var _result = (vfIdx!=null) ? (VF._results||[]).find(function(r){return r.idx===vfIdx;}) : null;
    var _tryRegen = function(reason){
      if (!_result || _result.page_idx==null || _result.panel_idx==null) {
        imgEl.style.opacity = '0.15'; imgEl.title = 'File not found (再生成不可・ページ情報なし): ' + fname;
        imgEl._recovering = false;
        return;
      }
      _result._regenAttempts = (_result._regenAttempts||0) + 1;
      if (_result._regenAttempts > 3) {
        imgEl.style.opacity = '0.15'; imgEl.title = '再生成3回失敗: ' + fname;
        imgEl._recovering = false;
        console.warn('[LINK_RECOVER_V2_AUTOREGEN] give up after 3 attempts', fname);
        return;
      }
      console.warn('[LINK_RECOVER_V2_AUTOREGEN] ' + reason + ' -> auto regenerate page='+_result.page_idx+' panel='+_result.panel_idx+' attempt='+_result._regenAttempts);
      imgEl.title = '🔄 自動再生成中(試行'+_result._regenAttempts+'/3)...';
      Promise.resolve()
        .then(function(){
          var pn = window._pagesData && window._pagesData[_result.page_idx] && window._pagesData[_result.page_idx].panels[_result.panel_idx];
          if (pn) { pn.image_path = null; pn._img_manual_selected = false; }
          return generateSinglePanel(_result.page_idx, _result.panel_idx);
        })
        .then(function(){
          var pn = window._pagesData && window._pagesData[_result.page_idx] && window._pagesData[_result.page_idx].panels[_result.panel_idx];
          var newPath = pn && pn.image_path;
          if (newPath) {
            _result.image_path = newPath; _result.ok = true; _result.err = '';
            var newUrl = (newPath.indexOf('/output/')===0 ? API + newPath : API + '/api/image?path=' + encodeURIComponent(newPath)) + '&v=' + Date.now();
            imgEl.src = newUrl; imgEl.style.opacity = '1'; imgEl.title = '✅ 自動再生成で復旧済み';
            imgEl._recovering = false;
            try { VF.renderGallery(); } catch(_e){}
            VF._persistResults && VF._persistResults();
          } else {
            imgEl._recovering = false;
            setTimeout(function(){ _tryRegen('regenerate completed but no image_path'); }, 2000);
          }
        })
        .catch(function(e){
          console.error('[LINK_RECOVER_V2_AUTOREGEN] regenerate failed', e);
          imgEl._recovering = false;
          setTimeout(function(){ _tryRegen('regenerate threw error: ' + (e&&e.message||e)); }, 3000);
        });
    };
    if (!fname || fname.length < 5) { imgEl._recovering = false; return; }
    fetch(API + '/api/find-output?name=' + encodeURIComponent(fname))
        .then(function(r){ return r.json(); })
        .then(function(d){
            if (d.image_path) {
                var newUrl = API + d.image_path;
                var probe = new Image();
                probe.onload = function(){
                    imgEl.src = newUrl;
                    imgEl.style.opacity = '1';
                    imgEl.title = '✅ ファイル再スキャンで復旧済み';
                    imgEl._recovering = false;
                    var fname2 = d.image_path.split('/').pop();
                    VF._results.forEach(function(r){
                        if (r.image_path && r.image_path.split('/').pop() === fname2) {
                            r.image_path = d.image_path;
                        }
                    });
                    VF._persistResults && VF._persistResults();
                    console.log('[LINK_RECOVER_V1] Recovered:', failedUrl, '->', newUrl);
                };
                probe.onerror = function(){ _tryRegen('rescan found path but file unreadable: ' + newUrl); };
                probe.src = newUrl;
            } else {
                _tryRegen('rescan found nothing for ' + fname);
            }
        })
        .catch(function(){ _tryRegen('find-output request failed for ' + fname); });
},
// [LINK_RECOVER_V2_AUTOREGEN 2026-10-14] VF._results保存の共通化（既存で複数箇所に
// 散らばっていたマージ保存ロジックを1関数に集約）。
_persistResults: function(){
    try {
      var _lrSv = {}; try{ _lrSv = JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(_lrE){}
      _lrSv.results = VF._results;
      localStorage.setItem('_vf_results', JSON.stringify(_lrSv));
    } catch(_lrE2) { console.warn('[LINK_RECOVER_V2_AUTOREGEN] persist failed', _lrE2); }
},
renderGallery: function(){
      var g = document.getElementById('vf_gallery'); if(!g) return;
      var rs = VF._results; if(!rs.length && !VF._cacheCleared){ var sv=localStorage.getItem('_vf_results'); if(sv){ try{ var o=JSON.parse(sv); rs=o.results||[]; VF._results=rs; }catch(e){} } }
      // NO_FLICKER_V1: カード単位で差分更新。画像URLは image_path が変わった時だけ変える（毎回 Date.now() を付けない）
      var seen = {};
      rs.forEach(function(r){
        var key = 'vfcard_'+r.idx; seen[key]=1;
        var url = r.image_path ? ((r.image_path.indexOf('/output/')===0) ? API + r.image_path : API + '/api/image?path=' + encodeURIComponent(r.image_path)) : '';
        var sig = url+'|'+(r.ok?1:0)+'|'+(r.err||'')+'|'+r.sec+'|'+(r.video||'');
        var card = document.getElementById(key);
        if (card && card.dataset.sig === sig) return;   // 変化なし → 触らない
        var _vurl = r.video ? (API + (r.video.startsWith('/') ? r.video : '/output/videos/' + r.video.split('/').pop())) : '';
        var _vsig = _vurl ? '|vid:'+r.video : '';
        var html =
          // === メイン画像 ===
          // [EM_LIGHTBOX_V1 2026-10-05] ユーザー指摘「拡大されるけど前後移動等の機能がない」。
          // 従来は onclick="window.open(this.src,'_blank')" で別タブに画像だけ開いていた。
          // rewire()がこのonclickを後から上書きする設計だったが確実性に欠けるため、生成時点
          // から window.vfLBOpen を直接呼ぶようにする(tkLBベースの前/次/閉じるライトボックス)。
          (url ? '<img src="'+url+'" loading="lazy" data-vfidx="'+r.idx+'" style="width:100%;aspect-ratio:3/4;object-fit:cover;display:block;cursor:zoom-in" onclick="window.vfLBOpenByIdx&&window.vfLBOpenByIdx('+r.idx+')" onerror="VF.recoverImg(this,this.src,'+r.idx+')">' : '<div style="width:100%;aspect-ratio:3/4;display:flex;align-items:center;justify-content:center;color:#f87171;font-size:12px">失敗<br>'+(r.err||'')+'</div>')
          // === ラベル行 ===
          + '<div style="padding:5px 8px 3px;font-size:11px;color:#cbd5e1;display:flex;align-items:flex-start;gap:4px" title="'+(r.label||'').replace(/"/g,'&quot;')+'"><b style="color:#93c5fd;flex-shrink:0">'+(r.idx+1)+'</b><span style="flex:1;min-width:0;white-space:normal;word-break:break-word;line-height:1.3">'+(r.label||'')+'</span><span style="color:#6b7280;flex-shrink:0">'+r.sec+'s</span></div>'
          // === 動画セクション ===
          + (_vurl
            ? '<div style="background:#020617;border-top:1px solid #1f2937">'
              + '<video src="'+_vurl+'" controls muted playsinline loop style="width:100%;max-height:180px;display:block;background:#000" preload="none"></video>'
              + '<div style="padding:2px 6px 4px;display:flex;gap:4px;align-items:center">'
              + '<span style="font-size:10px;color:#34d399;flex:1">🎬 '+(r.video||'').split('/').pop().slice(0,28)+'</span>'
              + '<a href="'+_vurl+'" download style="font-size:11px;padding:2px 8px;background:#065f46;color:#6ee7b7;border:1px solid #047857;border-radius:4px;text-decoration:none;white-space:nowrap">⬇ DL</a>'
              + '<button onclick="vfDeleteVideo(\''+r.idx+'\')" style="font-size:11px;padding:2px 6px;background:#3b0a0a;color:#fca5a5;border:1px solid #7f1d1d;border-radius:4px;cursor:pointer" title="動画を削除">🗑</button>'
              + '</div></div>'
            : '<div style="padding:4px 6px;border-top:1px solid #111827">'
              + '<button id="vfmkbtn_'+r.idx+'" onclick="vfMakeVideo('+r.idx+')" style="width:100%;padding:6px 10px;background:linear-gradient(90deg,#78350f,#d97706);color:#fff;border:none;border-radius:5px;cursor:pointer;font-size:12px;font-weight:700">🎬 動画生成</button>'
              + '</div>')
          // [SINGLE_PANEL_MODE_BTNS_V1 2026-10-09] ユーザー要望: 今このコマが静止画用/動画素材用
          // どちらを生成しているのか分かりづらい → 明示的に選べる2ボタンのみにする。
          // 旧「🎨このコマだけ再生成」(VF_SINGLE_REGEN_BTN_V1 2026-10-06)はユーザー指示により削除。
          + ((r.page_idx!=null && r.panel_idx!=null)
            // [SINGLE_PANEL_BTN_SEPARATE_FIX_V1 2026-10-09] ユーザー報告(スクショ確認):
            // 旧実装はgenerateSinglePanel内のボタン無効化セレクタが部分文字列マッチ
            // (`onclick*="generateSinglePanel(${pgIdx},${pnIdx}"`)だったため、
            // "generateSinglePanel(0,0,false)"と"generateSinglePanel(0,0,true)"の
            // 両方にマッチしてしまい、静止画ボタンを押すと動画ボタンも一緒に
            // 「生成中…」表示になっていた(逆方向も同様)。data-vfmode属性で明確に
            // 区別し、無効化対象をモード別に限定する。
            ? '<div style="padding:2px 6px 2px;display:flex;gap:4px">'
              + '<button data-vfmode="still" data-vfpg="'+r.page_idx+'" data-vfpn="'+r.panel_idx+'" onclick="generateSinglePanel('+r.page_idx+','+r.panel_idx+',false)" title="\u9759\u6b62\u753b\u7528\u306e\u69cb\u56f3\u3067\u751f\u6210\uff08\u30ab\u30e1\u30e9\u89d2\u5ea6\u56fa\u5b9a\uff09" style="flex:1;font-size:11px;padding:5px 4px;background:linear-gradient(90deg,#1e3a5f,#2563eb);color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:700">\ud83d\uddbc \u9759\u6b62\u753b1\u679a</button>'
              + '<button data-vfmode="video" data-vfpg="'+r.page_idx+'" data-vfpn="'+r.panel_idx+'" onclick="generateSinglePanel('+r.page_idx+','+r.panel_idx+',true)" title="\u52d5\u753b\u7d20\u6750\uff08i2v\uff09\u7528\u306e\u69cb\u56f3\u30d0\u30ea\u30a8\u30fc\u30b7\u30e7\u30f3\u3067\u751f\u6210" style="flex:1;font-size:11px;padding:5px 4px;background:linear-gradient(90deg,#78350f,#d97706);color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:700">\ud83c\udfac \u52d5\u753b\u7d20\u67501\u679a</button>'
              + '</div>'
            : '')
          // === AIコピーボタン ===
          + '<div style="padding:4px 6px 3px"><button class="vfCopyBtn" onclick="vfPanelCopy('+r.idx+','+(r.page_idx!=null?r.page_idx:-1)+','+(r.panel_idx!=null?r.panel_idx:-1)+')" style="width:100%;font-size:11px;padding:6px 6px;background:linear-gradient(90deg,#2563eb,#3b82f6);color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:600">\ud83e\udd16 AI\u306b\u6295\u3052\u308b\u60c5\u5831\u3092\u30b3\u30d4\u30fc</button></div>'
              + '<div style="padding:0 6px 6px"><button onclick="vfPanelLog('+(r.page_idx!=null?r.page_idx:r.idx)+')" style="width:100%;font-size:11px;padding:6px 6px;background:#334155;color:#cbd5e1;border:1px solid #475569;border-radius:6px;cursor:pointer;font-weight:600">LOG</button></div>'
        if (!card) { card = document.createElement('div'); card.id = key; card.style.cssText='background:#0b1220;border-radius:8px;overflow:hidden'; }
        // RG_INNERHTML_FIX_V1: 組み立てた html をカードに反映（欠落していたため全カードが空＝黒だった）
        card.innerHTML = html; card.dataset.sig = sig; card.dataset.idx = r.idx;
        // idx 順に配置
        var placed=false; for (var c=g.firstElementChild; c; c=c.nextElementSibling) { if (c!==card && parseInt(c.dataset.idx||'-1',10) > r.idx) { g.insertBefore(card, c); placed=true; break; } }
        if (!placed && card.parentNode!==g) g.appendChild(card);
      });
      Array.prototype.slice.call(g.children).forEach(function(c){ if (!seen[c.id]) c.remove(); });
      vfUpdateVideoGallery();
    },
    pdf: async function(){
      var rs = VF._results.filter(function(r){return r.ok;});
      if (!rs.length) { alert('PDFにする画像がありません'); return; }
      var sv = {}; try{ sv=JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){}
      var pages = rs.map(function(r,i){ return { page:i, background_note:'', panels:[{ image_path:r.image_path, dialogue:(r.idx+1)+' '+(r.label||''), page_idx:i, panel_idx:0 }] }; });
      var ckpt = sv.ckpt ? ((typeof STYLE_PRESETS!=='undefined' && STYLE_PRESETS[sv.ckpt] && STYLE_PRESETS[sv.ckpt].label) || sv.ckpt) : (document.getElementById('checkpoint')?.value||'').replace(/\.safetensors$/,'');
      var title = '検証 '+(sv.label||'')+(ckpt?' ['+ckpt+']':'');
      VF.setStatus('PDF生成中…');
      try {
        var res = await fetch(API+'/api/pdf', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({pages:pages, title:title, author:'VERIFY', mosaic_level:'off'})});
        if (res.ok && (res.headers.get('content-type')||'').indexOf('application/pdf')>=0) {
          var blob = await res.blob(); var a=document.createElement('a'); a.href=URL.createObjectURL(blob);
          a.download = 'verify_'+(sv.char||'char')+(ckpt?'_'+ckpt:'')+'.pdf'; a.click();
          VF.setStatus('PDF出力完了: '+a.download);
        } else { var d=await res.json().catch(function(){return {};}); VF.setStatus('PDF失敗: '+(d.error||res.status)); }
      } catch(e){ VF.setStatus('PDF失敗: '+e.message); }
    },
    // [VF_STEP5_SELL_V1 2026-10-05] 「まとめてPDF」(画像)の販売フローと同じ考え方で、
    // 各コマの動画(STEP4で生成済み)を1本に連結して販売用動画パッケージを作る。
    // サーバー側 /api/vf-concat-video (talk_motion.concat_fx を使用)を叩く。
    concatVideo: async function(){
      var rs = (VF._results||[]).filter(function(r){ return r.ok && r.video; });
      if (!rs.length) { alert('連結できる動画がありません（STEP4で先に各コマの動画を生成してください）'); return; }
      var sv = {}; try{ sv=JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){}
      var ckpt = sv.ckpt ? ((typeof STYLE_PRESETS!=='undefined' && STYLE_PRESETS[sv.ckpt] && STYLE_PRESETS[sv.ckpt].label) || sv.ckpt) : (document.getElementById('checkpoint')?.value||'').replace(/\.safetensors$/,'');
      var outName = 'verify_video_'+(sv.char||'char')+(ckpt?'_'+ckpt:'')+'_'+Date.now().toString(36);
      var btn = document.getElementById('vf_concatVideoBtn');
      if (btn) { btn.disabled = true; btn.textContent = '⏳ 連結中…'; }
      VF.setStatus('動画を連結中… ('+rs.length+'本)');
      try {
        // [VF_STEP5_SELL_V1] 既存の /api/motion/concat (talk_motion.concat_fx、トランジション連結+BGM自動選曲)
        // をそのまま流用。新規エンドポイントを増やさず実績のある処理を再利用する。
        var videos = rs.map(function(r){ return r.video; });
        var res = await fetch(API+'/api/motion/concat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({videos: videos, out_name: outName, title: sv.label||'', transition: 'dissolve', dur: 0.5, bgm: 'auto'})});
        var j = await res.json();
        if (j.error) throw new Error(j.error);
        VF.setStatus('🎬 動画連結完了: '+(j.video_url||'').split('/').pop());
        if (j.video_url) {
          var a = document.createElement('a'); a.href = API + j.video_url; a.download = outName + '.mp4';
          document.body.appendChild(a); a.click(); a.remove();
        }
      } catch(e) {
        VF.setStatus('動画連結失敗: ' + e.message);
        alert('動画連結失敗: ' + e.message);
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = '🎬 まとめて動画（1本に連結）'; }
      }
    },
    // [HTML_VIDEO_EXPORT_V1 2026-10-05] コマ毎に静止画+動画(あれば)をインライン再生できる
    // スタンドアロンHTMLビューアをZIPで出力する（FANZA/DLsite/BASE向け、PDFの代替）。
    // サーバー側 /api/export-html-video を叩き、/api/download/html-video/{filename} でDLする。
    exportHtmlVideo: async function(){
      var target = prompt('出力先を選んでください（fanza / dlsite / base）', 'fanza');
      if (!target) return;
      target = String(target).trim().toLowerCase();
      if (['fanza','dlsite','base'].indexOf(target) === -1) target = 'generic';
      var btn = document.getElementById('vf_htmlVideoBtn');
      if (btn) { btn.disabled = true; btn.textContent = '⏳ HTML版を生成中…'; }
      VF.setStatus('コマ動画入りHTML版を生成中…('+target+')');
      try {
        var res = await fetch(API+'/api/export-html-video', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({target: target})});
        var j = await res.json();
        if (j.error) throw new Error(j.error);
        if (!j.ok) throw new Error('生成に失敗しました');
        // [HTML_VIDEO_ONLY_FILTER_V1 2026-10-14] 動画ありコマが1つもない場合は明示的に警告（空ZIP回避の案内）
        if (!j.panels_with_video) { VF.setStatus('⚠ 動画ありコマが0件のためHTML版は作成されませんでした（全'+j.panels_total+'コマ中 動画0件）'); alert('動画ありコマが0件のため、HTML版は作成されませんでした。\nSTEP4で各コマの動画を生成してから再実行してください。'); if (btn) { btn.disabled = false; btn.textContent = '🎞 コマ動画入りHTML版を作る（FANZA/DLsite/BASE用ZIP）'; } return; }
        VF.setStatus('🎞 HTML版出力完了: '+j.zip_path+'（全'+j.panels_total+'コマ中 '+j.panels_with_video+'コマに動画あり・動画なしコマは除外済み）');
        var url = API + '/api/download/html-video/' + encodeURIComponent(j.zip_path);
        var a = document.createElement('a'); a.href = url; a.download = j.zip_path;
        document.body.appendChild(a); a.click(); a.remove();
      } catch(e) {
        VF.setStatus('HTML版出力失敗: ' + e.message);
        alert('HTML版出力失敗: ' + e.message);
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = '🎞 コマ動画入りHTML版を作る（FANZA/DLsite/BASE用ZIP）'; }
      }
    },
    // VF_CLEAR_CONFIRM_V2: ブラウザ confirm() が即閉じる環境向けに自前ダイアログ
    askClear: function(){
      var msg = VF._running ? '生成中です。停止して検証結果をクリアしますか？' : '検証結果をクリアしますか？';
      var old=document.getElementById('vfClearDlg'); if(old) old.remove();
      var d=document.createElement('div'); d.id='vfClearDlg';
      d.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2147483600;display:flex;align-items:center;justify-content:center';
      d.innerHTML='<div style="background:#111827;color:#f3f4f6;border:1px solid #374151;border-radius:12px;padding:20px 24px;min-width:320px;max-width:90vw;box-shadow:0 10px 40px #000a;font-size:14px">'
        +'<div style="font-weight:700;font-size:15px;margin-bottom:8px">🧹 クリア</div>'
        +'<div style="color:#d1d5db;line-height:1.6">'+msg+'<br><small style="color:#9ca3af">左リストの✅/❌・右ギャラリー・保存済み進捗を消し、元のページデータがあれば復元します。生成済み画像ファイル自体は消えません。</small></div>'
        +'<div style="display:flex;gap:8px;justify-content:flex-end;margin-top:16px"><button id="vfClearNo" style="padding:8px 16px;background:#374151;color:#e5e7eb;border:0;border-radius:8px;cursor:pointer">キャンセル</button><button id="vfClearYes" style="padding:8px 16px;background:#dc2626;color:#fff;border:0;border-radius:8px;font-weight:700;cursor:pointer">クリアする</button></div></div>';
      document.body.appendChild(d);
      d.querySelector('#vfClearNo').onclick=function(){ d.remove(); };
      d.querySelector('#vfClearYes').onclick=function(){ d.remove(); VF.clear(true); };
      d.addEventListener('click',function(e){ if(e.target===d) d.remove(); });
    },
    clear: function(force){
      if(!force){ VF.askClear(); return; }
      // VF_CLEAR_FIX 2026-09-25: 実行中ループを止め、ボタン状態を初期化
      VF._stop=true; VF._running=false; VF._cleared=true;
      // [VF_CLEAR_STOPFLAG_FIX_V1 2026-10-06] ユーザー報告:
      // 「クリアボタンでリクエストキャンセルするロジックが機能してない」
      // (クリア直後に/api/generate-panelが勝手に発火し500エラー)。
      // 根本原因: clear()はVF._userStoppedを立てておらず、startComfyWatchの
      // AUTO_RESUME_ANY_V1(VF._running===false && !VF._userStopped && 未完了残あり
      // なら20秒後に自動でVF.hdrResume()を呼ぶ)のタイマーが既にアーム済みの場合、
      // クリアでlocalStorageの_vf_resultsを消してもタイマー自体は止まらず、
      // 20秒後に古い状態を元に再開を試みて失敗していた。
      // 対策: 手動停止と同じ扱いにしてVF._userStopped=trueを立て、
      // 関連するアーム状態(_armedAny/_resumeArmed/_hangArmed/_cqArmed/_cqPid)も
      // 明示的にリセットする。
      VF._userStopped=true; VF._haltedByComfy=false;
      VF._armedAny=0; VF._resumeArmed=0; VF._hangArmed=0; VF._cqArmed=0; VF._cqPid=null;
      // VF_CLEAR_FORCE_CANCEL_V1 2026-10-03: クリア時にComfyUI側の進行中リクエストも強制キャンセル
      try { fetch((window.API||API)+'/api/stop',{method:'POST'}).catch(function(){}); } catch(e){}
      try { var rb=document.getElementById('vf_runBtn'), sb=document.getElementById('vf_stopBtn'); if(rb){rb.disabled=false;rb.style.opacity=1;} if(sb){sb.disabled=true;sb.style.opacity=.5;} } catch(e){}
      VF._results=[]; localStorage.removeItem('_vf_results'); VF.renderGallery(); VF.setStatus('',0);
      var bk = window._vfBackupPages || localStorage.getItem('_vfBackupPages');
      if (bk) { try { window._pagesData = JSON.parse(bk); localStorage.setItem('_pagesData', bk); localStorage.setItem('pagesData', bk); renderPageList(window._pagesData); } catch(e){} window._vfBackupPages=null; localStorage.removeItem('_vfBackupPages'); }
      VF.previewOutfits();
    },
    // 保存済み結果から左リストの ✅/❌ を復元（リロード後も進捗が見えるように）
    restoreMarks: function(){
      var sv={}; try{ sv=JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){}
      var id = document.getElementById('vf_char').value;
      if (!sv.char || sv.char!==id) return;
      (sv.results||[]).forEach(function(r){ var rw=document.getElementById('vf_row_'+r.idx); if(rw) rw.querySelector('.vf_mark').textContent = r.ok?'✅':'❌'; });
      var n=(sv.results||[]).filter(function(r){return r.ok;}).length, tot=(sv.to||0)-(sv.from||1)+1;
      if (n && !VF._running) {
        VF.setStatus('前回: '+n+'/'+(tot>0?tot:'?')+' 成功（⏩続きから で再開 / 🧹クリアで初期化）', tot>0?Math.round(n/tot*100):0);
        // [VF_PAGELOAD_AUTO_RESUME_V1 2026-10-13] 従来はComfyUI停止→復帰時のみ自動再開し、
        // ページ再読み込み/タブを開き直した直後は手動で「続きから」を押す必要があり不便だった。
        // CONF落ち時に自動再起動(vf_autoRestart)がONかつ未完了が残っている場合、
        // ページロード時にも数秒待って自動的に続きから再開する。
        if (tot > 0 && n < tot) {
          var _arChk = document.getElementById('vf_autoRestart');
          if (!_arChk || _arChk.checked) {
            setTimeout(function(){
              if (!VF._running && !VF._userStopped) {
                try { VF.setStatus('⏩ ページ再読み込みを検知 → 自動で続きから再開…'); VF.run(true); } catch(e){ console.warn('[VF_PAGELOAD_AUTO_RESUME]', e); }
              }
            }, 3000);
          }
        }
      }
    }
  };
  // タブ切替時の初期化はボタン側 onclick で VF.init() を直接呼ぶ（switchTab ラップは読み込み順依存のため廃止）
  document.addEventListener('DOMContentLoaded', function(){ setTimeout(function(){ try{ if (document.getElementById('tab-verify')?.classList.contains('active')) VF.init(); VF.startComfyWatch(); }catch(e){} }, 1500); });
  if (document.readyState !== 'loading') setTimeout(function(){ try{ VF.startComfyWatch(); }catch(e){} }, 1500);
  // AUTO_RESUME_V1: 再起動/リロード時、未完了の連続生成があれば自動で「続きから」を再開（10秒カウントダウン・キャンセル可）
  VF.checkAutoResume = function(){
    try {
      var sv = {}; try{ sv = JSON.parse(localStorage.getItem('_vf_results')||'{}'); }catch(e){ return; }
      if (!sv || !sv.char || !sv.results) return;
      var from = parseInt(sv.from||1,10), to = parseInt(sv.to||0,10);
      var total = (to>0 ? (to-from+1) : (sv.results.length||0));
      var doneOk = (sv.results||[]).filter(function(r){ return r && r.ok && r.image_path; }).length;
      if (total<=0 || doneOk>=total) return;          // 全部完了済みなら何もしない
      if (VF._running) return;                          // 既に走っているなら不要
      if (sessionStorage.getItem('_vf_autoresume_done')==='1') return;  // 二重起動防止（同一タブ）
      var remain = total - doneOk;
      var bar = document.createElement('div');
      bar.id = '_vfAutoResumeBar';
      bar.style.cssText = 'position:fixed;left:50%;top:14px;transform:translateX(-50%);z-index:99999;background:linear-gradient(135deg,#1d4ed8,#0ea5e9);color:#fff;padding:12px 18px;border-radius:12px;box-shadow:0 6px 24px rgba(0,0,0,.45);font-size:14px;font-weight:700;display:flex;gap:12px;align-items:center';
      var sec = 10;
      var _cd = null;
      var cancel = function(){ if(_cd)clearInterval(_cd); bar.remove(); sessionStorage.setItem('_vf_autoresume_done','1'); };
      bar.innerHTML = '<span>⏳ 前回の続き（未完了 '+remain+'/'+total+' 件）を <b id="_vfArSec">'+sec+'</b> 秒後に自動再開します</span>'
        + '<button id="_vfArGo" style="height:30px;padding:0 14px;background:#16a34a;color:#fff;border:none;border-radius:7px;font-weight:800;cursor:pointer">▶ 今すぐ</button>'
        + '<button id="_vfArNo" style="height:30px;padding:0 14px;background:#7f1d1d;color:#fecaca;border:none;border-radius:7px;font-weight:800;cursor:pointer">✕ やめる</button>';
      document.body.appendChild(bar);
      var go = function(){ if(_cd)clearInterval(_cd); bar.remove(); sessionStorage.setItem('_vf_autoresume_done','1'); try{ VF.hdrResume(); }catch(e){ try{ switchTab('verify'); VF.init(); setTimeout(function(){ VF.run(true); },300); }catch(e2){} } };
      bar.querySelector('#_vfArGo').onclick = go;
      bar.querySelector('#_vfArNo').onclick = cancel;
      _cd = setInterval(function(){ sec--; var el=document.getElementById('_vfArSec'); if(el)el.textContent=sec; if(sec<=0){ go(); } }, 1000);
    } catch(e) {}
  };
  document.addEventListener('DOMContentLoaded', function(){ setTimeout(function(){ try{ VF.checkAutoResume(); }catch(e){} }, 3000); });
  if (document.readyState !== 'loading') setTimeout(function(){ try{ VF.checkAutoResume(); }catch(e){} }, 3000);
})();
