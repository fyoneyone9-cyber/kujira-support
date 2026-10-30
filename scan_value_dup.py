# 各ジャンル(S1..S10セット)の value 重複率と、本文の共有プレフィックス度を確認
import json,sys,collections,re,hashlib
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
sets=json.load(open(r'C:\AI\ComfyUI\outfit_sets.json',encoding='utf-8'))
GEN={
'babyreg':range(432,442),'breedfac':range(442,452),'lolify':range(452,462),'lolidoll':range(462,472),
'groom':range(472,482),'lolifuzoku':range(482,492),'tsugakuro':range(492,502),'lolipreg':range(502,512),
'lolifairy':range(512,522),'timestop':range(522,532),'lolisucc':range(532,542),'lolihypapp':range(542,552),
'kinshin':range(552,562),'kyoushi':range(562,572),'miko':range(572,582),'suimin':range(582,592),
'shouni':range(592,602),'hyoui':range(602,612),'aigan':range(612,622),'jitsufu':range(622,632),
'yousha':range(632,642),'rinjin':range(642,652),'shuukyou':range(652,662),'jinshin':range(662,672),
'harem12':range(412,422),'panchira':range(422,432),
}
for g,rng in GEN.items():
    vals=[]
    labs=[]
    nsets=0
    for i in rng:
        k=f'S{i:04d}'
        a=sets.get(k)
        if not a: continue
        nsets+=1
        items=a['items'] if isinstance(a,dict) else a
        for it in items:
            vals.append(it.get('value',''))
            labs.append(it.get('label',''))
    u=len(set(vals)); ul=len(set(labs))
    flag=' <<< VALUE-COPY' if vals and u<len(vals)*0.6 else ''
    print(f'{g}: sets={nsets} items={len(vals)} uniq_val={u} uniq_label={ul}{flag}')
    # sample first value of first set
    k=f'S{list(rng)[0]:04d}'
    a=sets.get(k); items=a['items'] if isinstance(a,dict) else a
    print('   ex:', items[0].get('label','')[:60],'||',items[0].get('value','')[:80])
