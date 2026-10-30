import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

# PayCube警告をPayCubeありの時だけ表示
old = "{!it.payment_received && payStatus !== '入金不要（無償）' && <p className=\"text-xs text-orange-400 font-bold\">?? PayCube\u306f\u5165\u91d1\u78ba\u8a8d\u5f8c\u306b\u767a\u6ce8</p>}"
new = "{!it.payment_received && payStatus !== '入金不要（無償）' && (it.equipment || []).some((e: {name?: string}) => e.name === 'PayCube') && <p className=\"text-xs text-orange-400 font-bold\">⚠️ PayCubeは入金確認後に発注</p>}"

# 実際のテキストで検索
marker = "PayCubeは入金確認後に発注"
idx = content.find(marker)
if idx < 0:
    # 旧テキスト
    marker2 = "PayCube\u306f\u5165\u91d1\u78ba\u8a8d\u5f8c\u306b\u767a\u6ce8"
    idx = content.find(marker2)

if idx >= 0:
    # 行全体を取得して置換
    start = content.rfind('\n', 0, idx) + 1
    end = content.find('\n', idx)
    old_line = content[start:end]
    print(f"found line: {repr(old_line)}")
    
    # payment_received チェックの行を特定して PayCube条件を追加
    if "payment_received" in old_line and "PayCube" in old_line:
        # equipment条件を追加
        new_line = old_line.replace(
            "payStatus !== '入金不要（無償）' &&",
            "payStatus !== '入金不要（無償）' && (it.equipment || []).some((e: {name?: string}) => e.name === 'PayCube') &&"
        )
        # テキストも修正
        new_line = new_line.replace(
            "?? PayCube\u306f\u5165\u91d1\u78ba\u8a8d\u5f8c\u306b\u767a\u6ce8",
            "⚠️ PayCubeは入金確認後に発注"
        )
        content = content[:start] + new_line + content[end:]
        print("OK")
    else:
        print(f"line content mismatch")
else:
    print("marker not found - searching...")
    # フォールバック: ?? で探す
    idx2 = content.find("PayCube")
    snippets = []
    i = 0
    while True:
        i = content.find("PayCube", i)
        if i < 0: break
        snippets.append((i, content[i:i+100]))
        i += 1
    for pos, s in snippets:
        if "入金" in s or "payment" in s:
            print(f"  pos={pos}: {repr(s)}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
