# -*- coding: utf-8 -*-
"""[KOUTEI_PRECISION_V1 2026-10-29] 工程管理表の判定精度を上げる。

これまで: CSVの equipment から雑に判定していた。
改善: 申込書を取り込んでいればそちらを優先する。
  申込書は費用明細なので「実際に発注した機材」が正確に分かる。

  申込書のキー -> 工程表の区分キー
    kiosk      -> kiosk（KIOSK）
    surface    -> surface（Surface / Windowsタブレット）
    paycube    -> paycube
    p400       -> p400
    passport   -> passport
    printer    -> printer（工程表には区分が無いが念のため）
    smartlock  -> smartlock
    pms        -> pms
    roomtablet -> roomtablet
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_koutei2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """                                                flags: {
                                                  pms: hasPms2,
                                                  cardkey: hasCard,
                                                  smartlock: hasLock2,"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                                // [KOUTEI_PRECISION_V1 2026-10-29] 申込書を取り込んでいれば
                                                //   そちらを優先する。費用明細なので実発注が正確に分かる。
                                                ...(() => {
                                                  let app: Record<string, number> = {}
                                                  try {
                                                    const raw = it.dashboard_todos?.['app_equips'] as string
                                                    if (raw) app = JSON.parse(raw)
                                                  } catch { /* 壊れていたら無視してCSV判定に落とす */ }
                                                  const hasApp = Object.keys(app).length > 0
                                                  return { _src: hasApp ? 'application' : 'csv' }
                                                })(),
                                                flags: (() => {
                                                  let app: Record<string, number> = {}
                                                  try {
                                                    const raw = it.dashboard_todos?.['app_equips'] as string
                                                    if (raw) app = JSON.parse(raw)
                                                  } catch { /* noop */ }
                                                  const A = (k: string) => !!app[k]
                                                  const hasApp = Object.keys(app).length > 0
                                                  // 申込書があればそれを優先、無ければ従来のCSV判定
                                                  return {
                                                  pms: hasApp ? A('pms') : hasPms2,
                                                  cardkey: hasApp ? A('cardkey') : hasCard,
                                                  smartlock: hasApp ? A('smartlock') : hasLock2,"""
s = s.replace(OLD, NEW, 1)

# flags の残りも申込書優先に
OLD2 = """                                                  keybox: equipItems.some(e => /キーボックス|keybox/i.test(e.name || '')),
                                                  kiosk: equipItems.some(e => /KIOSK|キオスク/i.test((e.name || '') + (e.value || ''))),
                                                  kiosk_desk: equipItems.some(e => /卓上/.test((e.name || '') + (e.value || ''))),
                                                  roomtablet: hasTablet,
                                                  surface: equipItems.some(e => /surface/i.test((e.name || '') + (e.value || ''))),
                                                  tablet: equipItems.some(e => /タブレット/.test(e.name || '')) && !hasTablet,
                                                  p400: hasP400,
                                                  paycube: hasPaycube,
                                                  paypay: hasPaypay,
                                                  sumaho: hasSumaho,
                                                  passport: equipItems.some(e => /パスポート/.test(e.name || '')),
                                                  hojokin: false,
                                                },"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                                  keybox: equipItems.some(e => /キーボックス|keybox/i.test(e.name || '')),
                                                  kiosk: hasApp ? A('kiosk')
                                                    : equipItems.some(e => /KIOSK|キオスク/i.test((e.name || '') + (e.value || ''))),
                                                  kiosk_desk: equipItems.some(e => /卓上/.test((e.name || '') + (e.value || ''))),
                                                  roomtablet: hasApp ? A('roomtablet') : hasTablet,
                                                  surface: hasApp ? A('surface')
                                                    : equipItems.some(e => /surface/i.test((e.name || '') + (e.value || ''))),
                                                  tablet: equipItems.some(e => /タブレット/.test(e.name || '')) && !hasTablet,
                                                  p400: hasApp ? A('p400') : hasP400,
                                                  paycube: hasApp ? A('paycube') : hasPaycube,
                                                  paypay: hasPaypay,
                                                  sumaho: hasSumaho,
                                                  passport: hasApp ? A('passport')
                                                    : equipItems.some(e => /パスポート/.test(e.name || '')),
                                                  hojokin: false,
                                                  }
                                                })(),"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
