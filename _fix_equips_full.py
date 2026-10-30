# -*- coding: utf-8 -*-
"""[CFG_EQUIPS_V2 2026-10-29] 設定コピーに工程管理用のキーを追加する。

指摘:「KIOSKとかチェック漏れしてるし大丈夫か？」
  → そのとおり。equips はヒアリングシート用のキーしか積んでいなかった。
     工程管理表には KIOSK / 卓上KIOSK / Surface / PayCube /
     パスポートリーダー / キーボックス / タブレット の区分があるのに
     1つも送っていなかったので、チェックが入らなかった。

対策: 申込書(app_equips)を最優先に、CSVも併用して全キーを積む。
  申込書は費用明細なので実発注が正確に分かる。

キー対応（工程管理表の区分）:
  04.PMS                -> pms
  05.カードキー          -> cardkey
  06.スマートロック      -> smartlock
  07.キーボックス        -> keybox
  08.KIOSK              -> kiosk
  09.卓上KIOSK          -> kiosk_desk
  10.ルームタブレット    -> roomtablet
  11.Surface            -> surface
  12.タブレット          -> tablet
  13.P400               -> p400
  14.PayCube            -> paycube
  15.PayPay             -> paypay
  16.スマホカード決済    -> sumaho
  17.パスポートリーダー  -> passport
  02.補助金             -> hojokin（判断材料が無いので送らない）
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_equips2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """                                      const equips: string[] = []
                                      if (hasPms2) equips.push('pms')
                                      if (hasLock2) equips.push('smartlock')
                                      if (hasCard) equips.push('cardkey')
                                      if (hasCyli) equips.push('cylinder')
                                      if (hasPaycube) equips.push('cash')
                                      if (hasP400) equips.push('p400')"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                      // [CFG_EQUIPS_V2 2026-10-29] ヒアリングシートと工程管理表の両方で使うキーを積む。
                                      //   申込書(app_equips)は費用明細なので実発注が正確。あればそちらを優先する。
                                      let APP: Record<string, number> = {}
                                      try {
                                        const raw = it.dashboard_todos?.['app_equips'] as string
                                        if (raw) APP = JSON.parse(raw)
                                      } catch { /* 壊れていたらCSV判定に落とす */ }
                                      const hasAPP = Object.keys(APP).length > 0
                                      const A = (k: string) => !!APP[k]
                                      const EQ = (re: RegExp) =>
                                        equipItems.some(e => re.test((e.name || '') + ' ' + (e.value || '')))

                                      const equips: string[] = []
                                      const add = (k: string, v: boolean) => { if (v) equips.push(k) }

                                      // --- ヒアリングシート用 ---
                                      add('pms',        hasAPP ? A('pms') : hasPms2)
                                      add('smartlock',  hasAPP ? A('smartlock') : hasLock2)
                                      add('cardkey',    hasAPP ? A('cardkey') : hasCard)
                                      add('cylinder',   hasCyli)
                                      add('cash',       hasAPP ? A('paycube') : hasPaycube)
                                      add('p400',       hasAPP ? A('p400') : hasP400)

                                      // --- 工程管理表用（これまで送っていなかった） ---
                                      add('kiosk',      hasAPP ? A('kiosk') : EQ(/KIOSK|キオスク/i))
                                      add('kiosk_desk', EQ(/卓上/))
                                      add('surface',    hasAPP ? A('surface') : EQ(/surface|Windowsタブレット/i))
                                      add('paycube',    hasAPP ? A('paycube') : hasPaycube)
                                      add('passport',   hasAPP ? A('passport') : EQ(/パスポート/))
                                      add('keybox',     EQ(/キーボックス|keybox/i))
                                      add('tablet',     EQ(/タブレット/) && !hasTablet && !EQ(/surface/i))"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
