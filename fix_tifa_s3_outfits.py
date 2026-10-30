"""
ティファS3のoutfitsが60シーン（旧30+新30の重複）になっているのを修正
旧シーンを削除して新30シーンだけにする
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

char_id = 'char_kakuseizai_s3_ff_tifa'
idx = content.find(f"id:'{char_id}'")
oi = content.find("outfits:", idx)
start = content.find('[', oi)

# ネストを追跡
depth = 0
in_string = False
string_char = None
i = start
while i < len(content):
    c = content[i]
    if in_string:
        if c == '\\':
            i += 2
            continue
        if c == string_char:
            in_string = False
    else:
        if c in ('"', "'"):
            in_string = True
            string_char = c
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    i += 1

current_outfits = content[start:end]

# 現在のoutfitsからlabelとvalueのペアを全部取得
items = re.findall(r"\{'label':'((?:[^'\\]|\\.)*?)','value':'((?:[^'\\]|\\.)*?)'\}", current_outfits)
print(f"Total items found: {len(items)}")

# 最初の30件のラベルを確認
for i, (label, val) in enumerate(items[:35]):
    print(f"  {i:02d}: {label[:50]}")

# 前半30件と後半30件で重複があるか確認
if len(items) == 60:
    front_labels = [items[i][0] for i in range(30)]
    back_labels = [items[i][0] for i in range(30, 60)]
    if front_labels == back_labels:
        print("\n前半30 == 後半30: 重複確認")
        # 旧S2コピー（前半）か新S3（後半）か判断
        # 新S3の特徴: 「静脈直撃」がindex 0にある
        if '静脈直撃' in front_labels[0]:
            print("前半が新S3シーン -> 前半30を残す")
            keep = items[:30]
        else:
            print("後半が新S3シーン -> 後半30を残す")
            keep = items[30:]
    else:
        print("\n前半≠後半: 重複なし確認")
        keep = items
elif len(items) > 30:
    print(f"\n{len(items)}件: 先頭30件だけ残す")
    # 新S3シーンを探す
    new_start = -1
    for i, (label, val) in enumerate(items):
        if '静脈直撃' in label:
            new_start = i
            break
    if new_start >= 0:
        keep = items[new_start:new_start+30]
        print(f"新S3シーン found at index {new_start}")
    else:
        keep = items[:30]
else:
    keep = items

print(f"\nKeeping {len(keep)} outfits")
for i, (label, val) in enumerate(keep):
    print(f"  {i:02d}: {label[:50]}")
