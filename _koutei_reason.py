# -*- coding: utf-8 -*-
"""[KOUTEI_REASON_V1 2026-10-29] 判定の根拠を表示する。

要望:「チェックしているものとチェックしていないもの、
      どのような判断でON/OFFなのかわかるようにして」

対策: ダッシュボード側で「なぜONか/なぜOFFか」を一緒に送り、
  ダイアログの各行に理由を出す。
  例:
    ✅ 08.KIOSK           申込書: KIOSK×2
    ✅ 06.スマートロック     CSV: スマートロック=EPIC
       05.カードキー        機材に無し
    ✅ 15.PayPay          常にON（判断材料なし）
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_reason_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """                                      const equips: string[] = []
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
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                      const equips: string[] = []
                                      // [KOUTEI_REASON_V1 2026-10-29] なぜON/OFFかを一緒に送り、
                                      //   ダイアログで根拠を表示できるようにする。
                                      const reasons: Record<string, string> = {}
                                      /** 申込書を優先して判定し、根拠を記録する */
                                      const addBy = (key: string, appKey: string | null,
                                                     csv: boolean, csvLabel: string) => {
                                        if (hasAPP && appKey) {
                                          if (APP[appKey]) {
                                            equips.push(key)
                                            reasons[key] = `申込書: ${appKey}×${APP[appKey]}`
                                          } else {
                                            reasons[key] = '申込書に記載なし'
                                          }
                                          return
                                        }
                                        if (csv) { equips.push(key); reasons[key] = `CSV: ${csvLabel}` }
                                        else reasons[key] = '機材に無し'
                                      }
                                      /** 常にONにするもの（判断材料が無い） */
                                      const addAlways = (key: string, why: string) => {
                                        equips.push(key); reasons[key] = why
                                      }

                                      // --- ヒアリングシート用 ---
                                      addBy('pms',       'pms',      hasPms2,  'PMSあり')
                                      addBy('smartlock', 'smartlock', hasLock2, 'スマートロックあり')
                                      addBy('cardkey',   'cardkey',  hasCard,  'カードキーあり')
                                      addBy('cylinder',  null,       hasCyli,  'シリンダー錠あり')
                                      addBy('cash',      'paycube',  hasPaycube, 'PayCubeあり')
                                      addBy('p400',      'p400',     hasP400,  'P400あり')

                                      // --- 工程管理表用 ---
                                      addBy('kiosk',      'kiosk',    EQ(/KIOSK|キオスク/i), 'KIOSKあり')
                                      addBy('kiosk_desk', null,       EQ(/卓上/), '卓上あり')
                                      addBy('surface',    'surface',  EQ(/surface|Windowsタブレット/i), 'Surfaceあり')
                                      addBy('paycube',    'paycube',  hasPaycube, 'PayCubeあり')
                                      addBy('passport',   'passport', EQ(/パスポート/), 'パスポートリーダーあり')
                                      addBy('keybox',     null,       EQ(/キーボックス|keybox/i), 'キーボックスあり')
                                      addBy('tablet',     null,       EQ(/タブレット/) && !hasTablet && !EQ(/surface/i), 'タブレット端末')"""
s = s.replace(OLD, NEW, 1)

# 常時ONの部分も理由付きに
OLD2 = """                                      if (hasTablet) equips.push('roomtablet')
                                      equips.push('sumaho')
                                      equips.push('paypay')
                                      // [V19] 工事シートは判断材料が無いので常にONにしておく
                                      equips.push('koji')"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                      addBy('roomtablet', 'roomtablet', hasTablet, 'ルームタブレットあり')
                                      addAlways('sumaho', '常にON（申込書から判断できないため）')
                                      addAlways('paypay', '常にON（申込書から判断できないため）')
                                      addAlways('koji',   '常にON（工事要否が判断できないため）')"""
s = s.replace(OLD2, NEW2, 1)

# cfg に reasons を含める
OLD3 = """                                        equips,
                                      }"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """                                        equips,
                                        reasons,
                                      }"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
