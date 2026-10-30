import sys
sys.stdout.reconfigure(encoding='utf-8')

INSERT_AFTER = '                print(f"[EXPR_REINJECT_V1] skip: {_er_e}", flush=True)\n\n            # POSE_PRESET_V1\n            try:\n                import pose_presets as _pp\n'
INSERT_AFTER_LINE = 48093

NEW_CODE = '''                print(f"[EXPR_REINJECT_V1] skip: {_er_e}", flush=True)

            # [POST_QR_DEDUPE_V1] EXPR_REINJECT/pos_add後の残留重複タグを再除去
            try:
                if "6" in wf:
                    import quality_rules as _qr2d
                    _d2_raw = wf["6"]["inputs"].get("text","") or ""
                    _d2_tags = _qr2d._split(_d2_raw)
                    _d2_rules = _qr2d._merge(_qr2d._load("_common"), _qr2d._load("real"))
                    _d2_prio = []
                    try:
                        _d2_prio_str = locals().get("_op_reinject","") or ""
                        if isinstance(_d2_prio_str, str):
                            for _dp in _qr2d._split(_d2_prio_str):
                                _dc = _qr2d._core(_dp)
                                if _dc: _d2_prio.append(_dc)
                    except Exception:
                        pass
                    _d2_log = []
                    _d2_tags = _qr2d._rule_dedupe_group(_d2_tags, _d2_rules.get("dedupe_groups"), _d2_log, _d2_prio)
                    _d2_tags = _qr2d._rule_dedupe(_d2_tags)
                    _d2_new = ", ".join(_d2_tags)
                    if _d2_new != _d2_raw:
                        wf["6"]["inputs"]["text"] = _d2_new
                        _before_c = len([x for x in _d2_raw.split(",") if x.strip()])
                        print(f"[POST_QR_DEDUPE_V1] {_before_c}->{len(_d2_tags)} tags / {len(_d2_raw)}->{len(_d2_new)}ch", flush=True)
            except Exception as _d2e:
                print(f"[POST_QR_DEDUPE_V1_ERR] {_d2e}", flush=True)
            # /POST_QR_DEDUPE_V1

            # POSE_PRESET_V1
            try:
                import pose_presets as _pp
'''

path = r'C:\AI\ComfyUI\api_server_3001.py'
with open(path, encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# 48093行目付近の正確な位置を特定してから置換
target_start = INSERT_AFTER_LINE - 1  # 0-indexed
# 前後5行を確認
print('=== 前後確認 ===')
for i in range(target_start-2, target_start+8):
    print(f'{i+1}: {lines[i]!r}')

# 対象箇所のテキストブロックを特定して置換
old_block = (
    '                print(f"[EXPR_REINJECT_V1] skip: {_er_e}", flush=True)\n'
    '\n'
    '            # POSE_PRESET_V1\n'
    '            try:\n'
    '                import pose_presets as _pp\n'
)

content = ''.join(lines)
count = content.count(old_block)
print(f'\\nblock count: {count}')

if count == 1:
    new_content = content.replace(old_block, NEW_CODE, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('OK: inserted POST_QR_DEDUPE_V1')
elif count == 2:
    # 1回目(48095付近)だけ置換する
    idx = content.find(old_block)
    new_content = content[:idx] + NEW_CODE + content[idx+len(old_block):]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('OK: inserted POST_QR_DEDUPE_V1 (first occurrence)')
else:
    print(f'ERROR: {count} occurrences found')
