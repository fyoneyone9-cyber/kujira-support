# -*- coding: utf-8 -*-
"""[HEARING_GAS_V13b] 進捗メッセージを実態に合わせる。
実測134秒だったので「30〜60秒」は嘘になっていた。
高速化後でも1〜2分かかる想定で案内する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
bak = P + ".bak_msg_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """  var step = sec < 8  ? '雛形をコピー中'
           : sec < 25 ? '不要なシートを削除中'
           :            '案件情報を入力中';
  document.getElementById('msg').innerHTML =
    '<b style="color:#1a73e8">⏳ ' + step + '…（' + sec + '秒）</b><br>' +
    '<span style="color:#888;font-size:12px">' +
    '全部で30〜60秒ほどかかります。この画面は閉じないでください</span>';"""
assert s.count(OLD) == 1, "anchor"
NEW = """  var step = sec < 10 ? '雛形をコピー中'
           : sec < 50 ? '不要なシートを削除中'
           :            '案件情報を入力中';
  // 目安90秒としてバーを進める（超えても止めない）
  var pct = Math.min(96, Math.round(sec / 90 * 100));
  document.getElementById('msg').innerHTML =
    '<b style="color:#1a73e8">⏳ ' + step + '…（' + sec + '秒）</b>' +
    '<div style="height:8px;background:#e0e0e0;border-radius:4px;margin:6px 0;overflow:hidden">' +
    '<div style="height:8px;width:' + pct + '%;background:#1a73e8;transition:width .4s"></div></div>' +
    '<span style="color:#888;font-size:12px">' +
    'シートを1枚ずつ削除するため1〜2分かかります。<br>' +
    'この画面は閉じないでください（閉じても処理自体は続きます）</span>';"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
