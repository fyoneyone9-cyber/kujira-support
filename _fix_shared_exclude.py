# -*- coding: utf-8 -*-
"""manual_due_date を兄弟同期の対象から除外する。
納品予定日は製品ごとに異なるため、同一現場でも揃えてはいけない。
SIBLING_SHARED_KEY の /_date$/ 系パターンに引っかからないか確認し、明示除外を入れる。"""
import io

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()

old = """  const SIBLING_SHARED_KEY = (k: string) =>
    /^manual_.*_status$/.test(k) ||          // P400/PayCube/VEGA3000 の手配状況"""
assert s.count(old) == 1, "anchor"
new = """  const SIBLING_SHARED_KEY = (k: string) =>
    // ⚠ manual_due_date(納品予定日)は製品ごとに異なるので同期対象外。
    //   下の /_date$/ 系パターンに巻き込まれないよう最初に除外する。
    k !== 'manual_due_date' && (
    /^manual_.*_status$/.test(k) ||          // P400/PayCube/VEGA3000 の手配状況"""
s = s.replace(old, new, 1)

old2 = """    k === 'keybox_status' || k === 'paypay_status' ||
    k === 'payment_status' || k === 'payment_memo'
"""
assert s.count(old2) == 1, "anchor2"
new2 = """    k === 'keybox_status' || k === 'paypay_status' ||
    k === 'payment_status' || k === 'payment_memo')
"""
s = s.replace(old2, new2, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("exclude added")
