with open(r'C:\Users\fyone\Desktop\teleapo_orig.tsx', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# OBJECTION_TREEを取得
tree_start = content.find('const OBJECTION_TREE')
# 終わりを探す（次のconstか関数定義）
import re
m = re.search(r'\n(const [A-Z]|function |type )', content[tree_start+100:])
if m:
    tree_end = tree_start + 100 + m.start()
    print('tree end at line:', content[:tree_end].count('\n')+1)
    tree_section = content[tree_start:tree_end]
    print('tree lines:', tree_section.count('\n'))
    # カテゴリ定義を探す
    cat_idx = tree_section.rfind("'cat_claim'")
    print('last cat at:', cat_idx)
    # 実際のデータ行数
    lines = tree_section.split('\n')
    print('total lines:', len(lines))
    # scriptタブの内容を確認
    script_idx = content.find("activeTab === 'script'")
    script_end = content.find("activeTab === 'yoneyama'")
    script_content = content[script_idx:script_end]
    print('\nscript tab lines:', script_content.count('\n'))
    print('script preview:', script_content[:300])
