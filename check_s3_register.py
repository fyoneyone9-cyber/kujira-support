import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# kakuseizai_s3 の CHAR_GROUP_DEFS / CHAR_CATEGORIES / registerGenre を確認
for kw in ['kakuseizai_s3', 'seizai_s3']:
    hits = [(m.start(), content[max(0,m.start()-20):m.start()+100]) for m in re.finditer(kw, content)]
    print(f"=== {kw} ({len(hits)}件) ===")
    for pos, s in hits[:8]:
        print(f"  pos={pos}: {repr(s)}")
    print()
