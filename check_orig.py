with open(r'C:\Users\fyone\Desktop\teleapo_orig.tsx', 'r', encoding='utf-8-sig') as f:
    content = f.read()

start = content.find('const OBJECTION_TREE')
end = content.find('export default function')
print('data section chars:', end-start)

# カテゴリ確認
import re
cats = re.findall(r"id: '(cat_[^']+)'", content)
print('categories:', cats[:20])

script_start = content.find("activeTab === 'script'")
print('script tab at line:', content[:script_start].count('\n')+1 if script_start > 0 else 'NOT FOUND')

yoneyama_tab = content.find("activeTab === 'yoneyama'")
print('yoneyama tab at line:', content[:yoneyama_tab].count('\n')+1 if yoneyama_tab > 0 else 'NOT FOUND')
