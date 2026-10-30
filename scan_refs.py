import re,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
s=open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8').read()
# where is S0432 defined (not referenced)
for m in re.finditer(r'"S0432"\s*:', s):
    print('def at', m.start())
    print(s[m.start()-200:m.start()+1500])
    print('---')
# also look for scene structures with value:
idx = s.find('SCENE_PRESETS')
print('SCENE_PRESETS idx:', idx)
for kw in ['OUTFIT_REF','_scene','scenes_ref','SCENES_REF']:
    print(kw, s.find(kw))
