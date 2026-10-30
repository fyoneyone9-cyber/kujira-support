import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ===== 現在のPOSE_TABLE再現 =====
POSE_TABLE = [
    ("spooning",       0, ["spooning", "spoon position"], ["side lying", "from behind"]),
    ("sixtynine",      1, ["69 position", "sixty-nine", "sixtynine"], []),
    ("fellatio",       2, ["fellatio", "penis in mouth", "blowjob", "oral sex", "deepthroat", "throat fuck", "irrumatio", "forced fellatio"], []),
    ("piledriver",     3, ["piledriver"], []),
    ("matingpress",    4, ["mating press"], []),
    ("standing",       5, ["standing sex", "against the wall", "pressed against wall", "pinned against wall", "wall sex", "standing from behind", "standing behind sex"], []),
    ("doggy",          6, ["doggy", "rear entry", "on all fours", "four legged stance", "face down ass up", "pov sex", "pov vaginal", "pov penetration", "sex from behind"], ["from behind", "bent over"]),
    ("cowgirl",        7, ["cowgirl", "girl on top", "straddling", "sitting on lap"], []),
    ("missionary",     8, ["missionary", "clothed sex", "sex in uniform", "cfnm"], ["on back", "lying", "legs up"]),
    ("analsex",        9, ["anal sex", "anal penetration", "anal creampie", "anal insertion", "anal fuck", "anal rape", "anal violation", "anus penetrated", "penis in anus", "ass spread and penetrated", "rear hole penetration"], []),
    ("paizuri",       10, ["paizuri", "titjob", "breast sex", "tit fuck", "boobjob", "boob job", "tittyfuck", "titty fuck", "penis between breasts"], []),
    ("fingering",     11, ["fingering", "finger penetration", "fingered", "finger inserted", "fingers inside", "digital penetration", "ass spread and spread open", "hole being spread", "anal spread"], []),
    ("scissoring",    12, ["scissoring", "tribbing"], []),
    ("doublepenet",   13, ["double penetration", "double vaginal", "double anal", "both holes filled", "vaginal and anal simultaneously"], []),
    ("eagle",         14, ["eagle position", "spread eagle"], []),
    ("facesitting",   15, ["face sitting", "facesitting", "sitting on face", "crotch over face", "sitting on his face"], []),
    ("gangbang",      16, ["gangbang", "spit roast", "spitroast", "multiple men"], []),
    ("fullnelson",    17, ["full nelson", "full nelson position"], []),
    ("pronebone",     18, ["prone bone", "prone bone position", "prone position on bed", "rear penetration", "lying prone penetration", "face down penetration", "utsub", "lying face down penetration", "fucked from behind while lying", "face down ass penetrated"], []),
    ("vibrator",      19, ["vibrator", "electric massager", "sex toy", "dildo", "toy insertion", "vibe inserted", "rotor", "magic wand", "plug inserted", "butt plug"], []),
    ("bukkake",       20, ["bukkake", "cum on face", "facial cumshot", "cum splattered", "covered in cum", "semen all over body", "body glazed with semen", "cum covered body", "semen splattered", "large creampie", "semen overflowing", "cum dripping from"], []),
    ("handjob",       21, ["handjob", "hand job", "stroking penis", "jerking off", "hand around penis", "fist around shaft"], []),
    ("footjob",       22, ["footjob", "foot job", "feet around penis", "soles around shaft"], []),
    ("intercrural",   23, ["intercrural", "thigh sex", "thigh job", "penis between thighs", "thighs squeezed around"], []),
    ("frenchkiss",    24, ["french kiss", "deep kiss", "making out", "kissing deeply", "tongue kiss", "open mouth kiss"], []),
    ("mutualmastur",  25, ["mutual masturbation", "both masturbating"], []),
    ("bondage",       26, ["bondage", "rope bondage", "shibari", "tied up", "restrained with rope", "wrists bound", "hands tied", "collar and leash", "leash pulled", "chained", "cuffed", "spread bar", "hogtied"], []),
    ("gagged",        27, ["mouth held open", "gag", "mouth gag", "ring gag", "open mouth gag", "forced mouth open", "jaw held open", "mouth spreader"], []),
    ("creampie_after",28, ["semen leaking", "cum leaking", "dripping from vagina", "dripping from anus", "creampie aftermath", "cum running down legs", "semen dripping down thigh", "overflow creampie"], []),
]

def detect_pose(val):
    low = val.lower()
    for pose, prio, exact, ambig in POSE_TABLE:
        for kw in exact:
            if kw in low:
                return pose, kw, prio
    return None, None, None

# ===== 誤発火リスク分析 =====
print("=" * 70)
print("【誤発火リスク分析】")
print("=" * 70)

risks = [
    # (テスト文字列, 期待pose, 説明)
    # --- large creampie → bukkake? ---
    ("large creampie, semen overflowing from vagina, missionary position",
     "missionary", "❗大量中出し: missionary期待だがbukkakeが先に火を噴く"),

    ("large creampie filled inside, cum dripping from vagina, lying on back",
     "creampie_after", "❗中出し後処理: creampie_after期待だがbukkake(prio20)が先"),

    # --- anal spread → fingering? ---
    ("ass exposed and spread open, ass spread, anus visible, no penetration",
     None, "❗肛門露出(挿入なし): fingering(anal spread)が誤発火しないか"),

    # --- collar and leash → bondage? ---
    ("leather collar fastened around neck, nude, kneeling, leash pulled",
     "bondage", "❗首輪拘束: bondageOKだがCTX_INJECTがrope/wrists tiedを注入"),

    # --- gag 単語 → gagged? ---
    ("gagging on penis, deepthroat, forced into mouth",
     "fellatio", "❗deepthroat: gagging含むがfellatio(prio2)が優先されるか"),

    ("choking, gagging from drug, dazed expression",
     "gagged", "❗薬物scene: gagging≠性的gag → gagged誤発火リスク"),

    # --- on all fours → doggy? (非性行為) ---
    ("on all fours, crawling on floor, no sex, fully clothed",
     None, "❗四つん這い: doggy固有語(on all fours)が非性行為でも発火"),

    # --- from behind + no sex → spooning曖昧語 ---
    ("standing from behind embrace, no penetration, romantic",
     "standing", "❗後ろから抱擁: standing固有語が発火(これはOK)"),

    # --- semen splattered → bukkake? (体全体) ---
    ("semen splattered all over body, not on face",
     "bukkake", "❗全身ぶっかけ: bukake発火→CTX_INJECTが顔射注入するか要確認"),

    # --- multiple men → gangbang? ---
    ("multiple men watching, not sex, spectators",
     "gangbang", "❗複数男性見学: multiple men → gangbang誤発火"),

    # --- spread eagle → eagle? ---
    ("spread eagle position, restrained, no sex act",
     "eagle", "❗開脚拘束: eagle発火→penetration系CTX_INJECTは無いのでOKか確認"),

    # --- making out → frenchkiss? (接吻のみ) ---
    ("making out, kissing, romantic, fully clothed",
     "frenchkiss", "❗接吻のみ: frenchkiss発火、これはOK"),

    # --- S2-19 body writing → 何も発火しないか ---
    ("body covered in writing, marker on skin, degradation text, nude",
     None, "S2-19落書き: 何も発火しない→fallback任せ（正常）"),

    # --- pronebone: rear penetration ambiguous ---
    ("rear penetration from below, lying on stomach, prone position on bed, creampie",
     "pronebone", "pronebone正常発火"),

    # --- creampie_after vs bukkake ---
    ("semen leaking from vagina, large creampie inside, lying limp",
     "bukkake", "❗中出し後: large creampie(prio20)でbukkake発火→顔射CTX_INJECT誤注入"),
]

print()
for val, expected, desc in risks:
    pose, kw, prio = detect_pose(val)
    ok = "✅" if pose == expected else ("⚠️ " if expected is None and pose is not None else "❌")
    mark = f"→ {pose}(kw='{kw}', prio={prio})" if pose else "→ None(fallback)"
    print(f"{ok} {desc}")
    print(f"   {mark}  | 期待: {expected}")
    print()

# ===== キーワード衝突チェック =====
print("=" * 70)
print("【キーワード重複・衝突チェック】")
print("=" * 70)
all_kws = {}
for pose, prio, exact, ambig in POSE_TABLE:
    for kw in exact:
        if kw in all_kws:
            print(f"❌ 重複KW: '{kw}' → {all_kws[kw]} AND {pose}(prio={prio})")
        else:
            all_kws[kw] = f"{pose}(prio={prio})"
print("(重複なければ表示なし)")
print()

# ===== 優先度が低すぎて死んでいるカテゴリ =====
print("=" * 70)
print("【creampie_after(prio=28) vs bukkake(prio=20) 競合】")
print("=" * 70)
test_cases = [
    "large creampie, semen leaking from vagina, prone position",
    "cum dripping from vagina, semen dripping down thigh",
    "semen overflowing, dripping from vagina",
]
for tc in test_cases:
    pose, kw, prio = detect_pose(tc)
    print(f"  '{tc[:60]}'")
    print(f"  → {pose} via '{kw}'")
    print()
