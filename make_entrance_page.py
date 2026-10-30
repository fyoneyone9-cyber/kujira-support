import sys, csv, os
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\fyone\Downloads\【工程管理】泰和アルン淀屋橋 - NW関連.csv'
with open(path, encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

# データ行（row2以降）
data = []
for r in rows[2:]:
    if len(r) < 7 or not r[6]:
        continue
    data.append({
        'room': r[6],
        'ap_wan_mac': r[7],
        'ap_lan_mac': r[8],
        'ap_pw': r[9],
        'ap_ip': r[10],
        'ap_ssid': r[11],
        'ap_wifi_pw': r[12],
        'ap_smart_connect': r[13],
        'ap_firmware': r[14],
        'ap_security': r[15],
        'sb_ssid': r[16],
        'sb_pw': r[17],
        'sb_stealth': r[18],
        'sb_id': r[19] if len(r) > 19 else '',
        'sb_wifi': r[20] if len(r) > 20 else '',
        'sb_firmware': r[21] if len(r) > 21 else '',
        'sb_updated': r[22] if len(r) > 22 else '',
    })

for d in data:
    print(d['room'], d['ap_ssid'], d['sb_id'])
print(f'total: {len(data)} rows')
