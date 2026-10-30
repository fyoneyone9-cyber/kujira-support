import sys, csv, json
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\fyone\Downloads\【工程管理】泰和アルン淀屋橋 - NW関連.csv'
with open(path, encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

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

data_json = json.dumps(data, ensure_ascii=False, indent=2)

tsx = f"""'use client'

import {{ useState }} from 'react'

const PROPERTY_NAME = '泰和アルン淀屋橋'

type RoomData = {{
  room: string
  ap_wan_mac: string
  ap_lan_mac: string
  ap_pw: string
  ap_ip: string
  ap_ssid: string
  ap_wifi_pw: string
  ap_smart_connect: string
  ap_firmware: string
  ap_security: string
  sb_ssid: string
  sb_pw: string
  sb_stealth: string
  sb_id: string
  sb_wifi: string
  sb_firmware: string
  sb_updated: string
}}

const DATA: RoomData[] = {data_json}

export default function EntrancePage() {{
  const [search, setSearch] = useState('')
  const [showPw, setShowPw] = useState(false)

  const filtered = DATA.filter(d =>
    d.room.includes(search) ||
    d.ap_ssid.toLowerCase().includes(search.toLowerCase()) ||
    d.sb_id.toLowerCase().includes(search.toLowerCase()) ||
    d.ap_ip.includes(search)
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 flex-wrap">
        <h1 className="text-2xl font-bold text-white">🏢 玄関集合機・NW管理</h1>
        <span className="text-slate-400 text-sm">{{PROPERTY_NAME}}</span>
        <span className="text-slate-500 text-xs">{{DATA.length}}部屋</span>
      </div>

      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder="部屋番号・SSID・SB-ID・IPで検索..."
          value={{search}}
          onChange={{e => setSearch(e.target.value)}}
          className="px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 text-sm w-72"
        />
        <button
          onClick={{() => setShowPw(v => !v)}}
          className={{`px-3 py-2 text-xs rounded-lg font-medium transition-colors ${{showPw ? 'bg-red-800 text-red-200' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}}`}}
        >
          {{showPw ? '🔓 PW表示中' : '🔒 PW非表示'}}
        </button>
        <span className="text-slate-500 text-xs">{{filtered.length}}件</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="text-slate-400 text-xs border-b border-slate-700">
              <th className="text-left py-2 px-3 whitespace-nowrap">部屋</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">📶 AP IP</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">SSID</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">WiFi PW</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">AP ログインPW</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">LAN MAC</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">WAN MAC</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">🤖 SB管理番号</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">SB更新日</th>
              <th className="text-left py-2 px-3 whitespace-nowrap">FW (AP)</th>
            </tr>
          </thead>
          <tbody>
            {{filtered.map((d, i) => (
              <tr key={{d.room}} className={{`border-b border-slate-800 hover:bg-slate-800/50 ${{i % 2 === 0 ? '' : 'bg-slate-900/30'}}`}}>
                <td className="py-2 px-3 font-bold text-white whitespace-nowrap">
                  {{d.room === '玄関集合機' || d.room === '宅配ボックス'
                    ? <span className="px-2 py-0.5 bg-blue-900 text-blue-200 rounded text-xs">{{d.room}}</span>
                    : d.room
                  }}
                </td>
                <td className="py-2 px-3 text-slate-300 font-mono text-xs whitespace-nowrap">{{d.ap_ip}}</td>
                <td className="py-2 px-3 text-slate-200 whitespace-nowrap">{{d.ap_ssid}}</td>
                <td className="py-2 px-3 font-mono text-xs whitespace-nowrap">
                  {{showPw
                    ? <span className="text-green-300">{{d.ap_wifi_pw}}</span>
                    : <span className="text-slate-600">••••••••</span>
                  }}
                </td>
                <td className="py-2 px-3 font-mono text-xs whitespace-nowrap">
                  {{showPw
                    ? <span className="text-yellow-300">{{d.ap_pw}}</span>
                    : <span className="text-slate-600">••••••••</span>
                  }}
                </td>
                <td className="py-2 px-3 text-slate-400 font-mono text-xs whitespace-nowrap">{{d.ap_lan_mac}}</td>
                <td className="py-2 px-3 text-slate-500 font-mono text-xs whitespace-nowrap">{{d.ap_wan_mac}}</td>
                <td className="py-2 px-3 whitespace-nowrap">
                  {{d.sb_id
                    ? <span className="px-2 py-0.5 bg-slate-700 text-slate-200 rounded font-mono text-xs">{{d.sb_id}}</span>
                    : <span className="text-slate-600 text-xs">—</span>
                  }}
                </td>
                <td className="py-2 px-3 text-slate-500 text-xs whitespace-nowrap">{{d.sb_updated}}</td>
                <td className="py-2 px-3 text-slate-600 text-xs whitespace-nowrap max-w-xs truncate">{{d.ap_firmware}}</td>
              </tr>
            ))}}
          </tbody>
        </table>
      </div>
    </div>
  )
}}
"""

out = r'C:\GensparkClaw\kujira-support\src\app\(app)\entrance\page.tsx'
import os; os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write(tsx)
print('written:', out)
