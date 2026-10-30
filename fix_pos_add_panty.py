"""
pos_addのパンティー汎用タグ問題を修正:
1. women's underwear / female panties / women's panties → 削除（色指定なしで品質低下）
2. clothed系との矛盾タグ bare crotch を conflicts に追加
3. panty_type dedupe グループに women's系を追加済みなのでdedupeは不要になる
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\quality_rules\real.json'
with open(path, encoding='utf-8') as f:
    d = json.load(f)

# 1. pos_add から色指定なし汎用パンティータグを削除
# (PAIPAN_FINAL_V1 が pubic タグを強制注入するので pos_add での重複も不要)
REMOVE_FROM_POS_ADD = {
    "women's underwear",
    "female panties", 
    "women's panties",
    # pubic hair 系も PAIPAN_FINAL_V1 が高重みで注入するので pos_add 側は削除
    "smooth hairless pubic area",
    "no pubic hair",
    "shaved pussy",
    "hairless pussy",
    # quality系は dedupe で1つに絞られるのでsharpnessグループの重複を減らす
    "8k resolution",
    "high definition",
    "crystal clear",
    "tack sharp",
    "fine detail",
    "highly detailed",
}
old_pos_add = d.get('pos_add', [])
new_pos_add = [t for t in old_pos_add if t not in REMOVE_FROM_POS_ADD]
d['pos_add'] = new_pos_add
print(f"pos_add: {len(old_pos_add)} -> {len(new_pos_add)}")
print("残り:", new_pos_add)

# 2. conflicts に bare_crotch_vs_clothed を追加
conflicts = d.get('conflicts', [])
# 既存チェック
existing = [c['name'] for c in conflicts]
print(f"\nexisting conflicts: {existing}")

if 'bare_crotch_vs_clothed' not in existing:
    conflicts.append({
        "name": "bare_crotch_vs_clothed",
        "prefer": "b",
        "a": [
            "bare crotch","exposed crotch","crotch exposed","naked crotch",
            "crotch visible","open crotch","bottomless"
        ],
        "b": [
            "panties under skirt","visible panties","wearing panties",
            "lower body fully clothed","legs covered","skirt on","pants on",
            "fully clothed","clothing intact"
        ]
    })
    d['conflicts'] = conflicts
    print("bare_crotch_vs_clothed conflict added")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f"\nSaved: {path}")
