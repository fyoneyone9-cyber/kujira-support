with open(r'C:\Users\fyone\Desktop\teleapo_orig.tsx', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# 行番号で各セクションを確認
for i, l in enumerate(lines):
    stripped = l.strip()
    if any(x in stripped for x in ['const OBJECTION_TREE', 'const CATEGORIES', 'const TABS', 'suggestByKeyword', 'export default', "activeTab === 'script'", "activeTab === 'yoneyama'"]):
        print(i+1, stripped[:80])
