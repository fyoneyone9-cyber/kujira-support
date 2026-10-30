import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\api_server_3001.py'
with open(path, encoding='utf-8') as f:
    content = f.read()

old = '''            # [KREA2_DUO_POS_INJECT] DUO時: 2人構図強化タグをPositiveに注入
            if _krea_has_duo and "6" in wf:
                _pos6_now = wf["6"]["inputs"].get("text", "")
                _duo_inject_tags = [
                    "(two girls in frame:1.9)",
                    "(both girls visible:1.9)",
                    "(two girls side by side:1.8)",
                    "(both faces visible:1.8)",
                ]
                _inject_str = "," + ",".join(_duo_inject_tags)
                if "(two girls in frame" not in _pos6_now and "(two girls visible" not in _pos6_now:
                    wf["6"]["inputs"]["text"] = _pos6_now + _inject_str
                    print(f"[KREA2_DUO_POS_INJECT] 2人構図タグ注入", flush=True)
                    _trace("KREA2_DUO_POS_INJECT", "2人構図タグ注入")
                else:
                    print(f"[KREA2_DUO_POS_INJECT] スキップ（既存タグあり）", flush=True)'''

new = '''            # [KREA2_DUO_POS_INJECT] DUO時: 2人構図強化タグをPositiveに注入
            # [DUO_INJECT_MALE_FIX_V1] male_scene=True(挿入/性行為)の場合は
            # "two girls" でなく "man and woman" 構図タグを使う（女性2人になるのを防ぐ）
            if _krea_has_duo and "6" in wf:
                _pos6_now = wf["6"]["inputs"].get("text", "")
                _duo_is_male_scene = _male_scene
                if _duo_is_male_scene:
                    _duo_inject_tags = [
                        "(man and woman:1.8)",
                        "(1boy 1girl:1.8)",
                        "(heterosexual couple:1.7)",
                        "(male and female:1.7)",
                    ]
                    _skip_key = "(man and woman"
                else:
                    _duo_inject_tags = [
                        "(two girls in frame:1.9)",
                        "(both girls visible:1.9)",
                        "(two girls side by side:1.8)",
                        "(both faces visible:1.8)",
                    ]
                    _skip_key = "(two girls in frame"
                _inject_str = "," + ",".join(_duo_inject_tags)
                if _skip_key not in _pos6_now:
                    wf["6"]["inputs"]["text"] = _pos6_now + _inject_str
                    _mode = "男女構図" if _duo_is_male_scene else "2人構図"
                    print(f"[KREA2_DUO_POS_INJECT] {_mode}タグ注入", flush=True)
                    _trace("KREA2_DUO_POS_INJECT", f"{_mode}タグ注入")
                else:
                    print(f"[KREA2_DUO_POS_INJECT] スキップ（既存タグあり）", flush=True)'''

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: replaced")
else:
    print("ERROR: not found")
