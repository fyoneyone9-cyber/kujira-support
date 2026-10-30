import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find first rohypnol_s2 char block and extract all outfit labels+values
# Look for char_rohypnol_s2_ and grab outfits array
idx = content.find('char_rohypnol_s2_jk_A')
if idx < 0:
    idx = content.find('char_rohypnol_s2_tifa')
chunk = content[idx:idx+60000]

# Extract all label/value pairs
pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,200}"value"\s*:\s*"([^"]{0,300})"', chunk)

POSE_TABLE = {
    'spooning':     ['spooning', 'spoon position'],
    'sixtynine':    ['69 position', 'sixty-nine', 'sixtynine'],
    'fellatio':     ['fellatio', 'penis in mouth', 'blowjob', 'oral sex', 'deepthroat', 'throat fuck', 'irrumatio', 'forced fellatio'],
    'piledriver':   ['piledriver'],
    'matingpress':  ['mating press'],
    'standing':     ['standing sex', 'against the wall', 'pressed against wall', 'wall sex', 'standing from behind', 'standing behind sex'],
    'doggy':        ['doggy', 'rear entry', 'on all fours', 'four legged stance', 'face down ass up', 'pov sex', 'pov vaginal', 'pov penetration', 'sex from behind'],
    'cowgirl':      ['cowgirl', 'girl on top', 'straddling', 'sitting on lap'],
    'missionary':   ['missionary', 'clothed sex', 'sex in uniform', 'cfnm'],
    'analsex':      ['anal sex', 'anal penetration', 'anal creampie', 'anal insertion', 'anal fuck', 'anal rape'],
    'paizuri':      ['paizuri', 'titjob', 'breast sex', 'tit fuck'],
    'fingering':    ['fingering', 'finger penetration', 'fingered'],
    'scissoring':   ['scissoring', 'tribbing'],
    'doublepenet':  ['double penetration', 'double vaginal', 'double anal'],
    'eagle':        ['eagle position'],
    'facesitting':  ['face sitting', 'facesitting'],
    'gangbang':     ['gangbang', 'spit roast'],
    'fullnelson':   ['full nelson'],
    'pronebone':    ['prone bone', 'prone bone position', 'prone position on bed', 'rear penetration', 'lying prone penetration', 'face down penetration', 'utsub'],
    'vibrator':     ['vibrator', 'electric massager', 'sex toy', 'dildo', 'toy insertion', 'vibe', 'rotor'],
    'bukkake':      ['bukkake', 'cum on face', 'facial cumshot'],
    'handjob':      ['handjob', 'hand job'],
    'footjob':      ['footjob', 'foot job'],
    'intercrural':  ['intercrural', 'thigh sex', 'thigh job'],
    'frenchkiss':   ['french kiss', 'deep kiss', 'making out', 'kissing deeply'],
    'mutualmastur': ['mutual masturbation'],
    'bondage':      ['bondage', 'rope bondage', 'shibari', 'tied up', 'restrained with rope'],
}

def detect_pose(val):
    low = val.lower()
    for pose, kws in POSE_TABLE.items():
        for kw in kws:
            if kw in low:
                return pose, kw
    return None, None

print('=== S2 outfit POSE_TABLE coverage check ===')
for label, val in pairs:
    if not label.startswith('S2-'):
        continue
    pose, kw = detect_pose(val)
    status = f'OK({pose} via "{kw}")' if pose else '❌ MISS'
    print(f'{label[:45]:50s} {status}')
    if not pose:
        print(f'  val: {val[:120]}')
