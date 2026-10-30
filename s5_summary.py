import io, re, collections
t = io.open(r'C:\GensparkClaw\kujira-support\s5_final.txt', encoding='utf-8', errors='ignore').read()
cur = None
pairs = collections.defaultdict(list)
seasons = {}
for line in t.splitlines():
    m = re.search(r'\[NG\]\s+(\S+)\s+seasons=\[([\d, ]+)\]', line)
    if m:
        cur = m.group(1)
        seasons[cur] = len(m.group(2).split(','))
    elif cur and '100%' in line:
        pairs[cur].append(line.strip())
print('total NG genres:', len(seasons))
for g in seasons:
    n = len(pairs[g]); ss = seasons[g]
    full = (n == ss*(ss-1)//2)
    print(('FULL-COPY' if full else 'PARTIAL '), g, 'seasons=%d dup_pairs=%d' % (ss, n))
