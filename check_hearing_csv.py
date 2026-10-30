import os, glob, csv, sys
sys.stdout.reconfigure(encoding='utf-8')

dst = r'C:\GensparkClaw\kujira-support\docs\hearing-sheet'
files = sorted(glob.glob(os.path.join(dst, '*.csv')))
for f in files:
    name = os.path.basename(f)
    print(f'\n=== {name} ===')
    try:
        with open(f, encoding='utf-8-sig', errors='replace') as fp:
            rows = list(csv.reader(fp))
        for row in rows[:15]:
            print(row)
    except Exception as e:
        print(f'ERROR: {e}')
