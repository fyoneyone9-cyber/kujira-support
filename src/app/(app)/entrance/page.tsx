'use client'

import { useState } from 'react'

const PROPERTY_NAME = '泰和アルン淀屋橋'

type RoomData = {
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
}

const DATA: RoomData[] = [
  {
    "room": "101",
    "ap_wan_mac": "EC-75-0C-22-4B-D3",
    "ap_lan_mac": "EC-75-0C-22-4B-D2",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.201",
    "ap_ssid": "TP-Link_4BD2",
    "ap_wifi_pw": "59251903",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB035",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/29"
  },
  {
    "room": "201",
    "ap_wan_mac": "98-BA-5F-23-1A-C6",
    "ap_lan_mac": "98-BA-5F-23-1A-C5",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.202",
    "ap_ssid": "TP-Link_1AC5",
    "ap_wifi_pw": "72989166",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB036",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "202",
    "ap_wan_mac": "60-83-E7-27-2A-2D",
    "ap_lan_mac": "60-83-E7-27-2A-2C",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.203",
    "ap_ssid": "TP-Link_2A2C",
    "ap_wifi_pw": "49375008",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB037",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "301",
    "ap_wan_mac": "30-68-93-8D-FB-D4",
    "ap_lan_mac": "30-68-93-8D-FB-D3",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.204",
    "ap_ssid": "TP-Link_FBD3",
    "ap_wifi_pw": "43951871",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB038",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "302",
    "ap_wan_mac": "98-BA-5F-23-23-00",
    "ap_lan_mac": "98-BA-5F-23-22-FF",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.205",
    "ap_ssid": "TP-Link_22FF",
    "ap_wifi_pw": "39863461",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB039",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "303",
    "ap_wan_mac": "98-BA-5F-23-2C-18",
    "ap_lan_mac": "98-BA-5F-23-2C-17",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.206",
    "ap_ssid": "TP-Link_2C17",
    "ap_wifi_pw": "15903662",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB040",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "401",
    "ap_wan_mac": "98-BA-5F-23-28-13",
    "ap_lan_mac": "98-BA-5F-23-28-12",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.207",
    "ap_ssid": "TP-Link_2812",
    "ap_wifi_pw": "31133395",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB041",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "402",
    "ap_wan_mac": "EC-75-0C-6C-32-F6",
    "ap_lan_mac": "EC-75-0C-6C-32-F5",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.208",
    "ap_ssid": "TP-Link_32F5",
    "ap_wifi_pw": "59864189",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB042",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "403",
    "ap_wan_mac": "30-68-93-8E-4E-F9",
    "ap_lan_mac": "30-68-93-8E-4E-F8",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.209",
    "ap_ssid": "TP-Link_4EF8",
    "ap_wifi_pw": "10657034",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB043",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "501",
    "ap_wan_mac": "30-68-93-8D-FC-CA",
    "ap_lan_mac": "30-68-93-8D-FC-C9",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.210",
    "ap_ssid": "TP-Link_FCC9",
    "ap_wifi_pw": "18386547",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB044",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "502",
    "ap_wan_mac": "30-68-93-8E-4E-AB",
    "ap_lan_mac": "30-68-93-8E-4E-AA",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.211",
    "ap_ssid": "TP-Link_4EAA",
    "ap_wifi_pw": "79404426",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB045",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "503",
    "ap_wan_mac": "98-BA-5F-23-30-B6",
    "ap_lan_mac": "98-BA-5F-23-30-B5",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.212",
    "ap_ssid": "TP-Link_30B5",
    "ap_wifi_pw": "15854834",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB046",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/28"
  },
  {
    "room": "601",
    "ap_wan_mac": "30-68-93-8E-4C-86",
    "ap_lan_mac": "30-68-93-8E-4C-85",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.213",
    "ap_ssid": "TP-Link_4C85",
    "ap_wifi_pw": "69817632",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB047",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "602",
    "ap_wan_mac": "30-68-93-8E-4F-0E",
    "ap_lan_mac": "30-68-93-8E-4F-0D",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.214",
    "ap_ssid": "TP-Link_4F0D",
    "ap_wifi_pw": "51045517",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB048",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "603",
    "ap_wan_mac": "98-BA-5F-23-28-FD",
    "ap_lan_mac": "98-BA-5F-23-28-FC",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.215",
    "ap_ssid": "TP-Link_28FC",
    "ap_wifi_pw": "44288549",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB049",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "701",
    "ap_wan_mac": "30-68-93-8E-4E-2A",
    "ap_lan_mac": "30-68-93-8E-4E-29",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.216",
    "ap_ssid": "TP-Link_4E29",
    "ap_wifi_pw": "49422269",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB050",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "702",
    "ap_wan_mac": "98-BA-5F-23-28-7F",
    "ap_lan_mac": "98-BA-5F-23-28-7E",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.217",
    "ap_ssid": "TP-Link_287E",
    "ap_wifi_pw": "16808423",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB051",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "703",
    "ap_wan_mac": "60-83-E7-27-2B-20",
    "ap_lan_mac": "60-83-E7-27-2B-1F",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.218",
    "ap_ssid": "TP-Link_2B1F",
    "ap_wifi_pw": "37717025",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB052",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "801",
    "ap_wan_mac": "98-BA-5F-23-52-2E",
    "ap_lan_mac": "98-BA-5F-23-52-2D",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.219",
    "ap_ssid": "TP-Link_522D",
    "ap_wifi_pw": "89847671",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB053",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "802",
    "ap_wan_mac": "30-68-93-8E-1F-0B",
    "ap_lan_mac": "30-68-93-8E-1F-0A",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.220",
    "ap_ssid": "TP-Link_1F0A",
    "ap_wifi_pw": "19069258",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB054",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "901",
    "ap_wan_mac": "98-BA-5F-23-49-CA",
    "ap_lan_mac": "98-BA-5F-23-49-C9",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.221",
    "ap_ssid": "TP-Link_49C9",
    "ap_wifi_pw": "12115969",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB055",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "902",
    "ap_wan_mac": "60-83-E7-27-29-94",
    "ap_lan_mac": "60-83-E7-27-29-93",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.222",
    "ap_ssid": "TP-Link_2993",
    "ap_wifi_pw": "70235821",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB056",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "1001",
    "ap_wan_mac": "EC-75-0C-6C-31-FD",
    "ap_lan_mac": "EC-75-0C-6C-31-FC",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.223",
    "ap_ssid": "TP-Link_31FC",
    "ap_wifi_pw": "56628890",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB057",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "1002",
    "ap_wan_mac": "98-BA-5F-23-21-B0",
    "ap_lan_mac": "98-BA-5F-23-21-AF",
    "ap_pw": "Vr7enqFU#2",
    "ap_ip": "192.168.100.224",
    "ap_ssid": "TP-Link_21AF",
    "ap_wifi_pw": "79711234",
    "ap_smart_connect": "〇",
    "ap_firmware": "1.0.4 Build 20241225 Rel. 58594(4A50)",
    "ap_security": "WPA3-パーソナル+WPA2-PSK[AES]",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "〇",
    "sb_id": "SB058",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "玄関集合機",
    "ap_wan_mac": "",
    "ap_lan_mac": "",
    "ap_pw": "",
    "ap_ip": "",
    "ap_ssid": "",
    "ap_wifi_pw": "",
    "ap_smart_connect": "",
    "ap_firmware": "",
    "ap_security": "",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "",
    "sb_id": "",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  },
  {
    "room": "宅配ボックス",
    "ap_wan_mac": "",
    "ap_lan_mac": "",
    "ap_pw": "",
    "ap_ip": "",
    "ap_ssid": "",
    "ap_wifi_pw": "",
    "ap_smart_connect": "",
    "ap_firmware": "",
    "ap_security": "",
    "sb_ssid": "kujira-sb",
    "sb_pw": "Kujiraadmin3313",
    "sb_stealth": "",
    "sb_id": "SB060",
    "sb_wifi": "〇",
    "sb_firmware": "〇",
    "sb_updated": "2025/05/30"
  }
]

export default function EntrancePage() {
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
        <span className="text-slate-400 text-sm">{PROPERTY_NAME}</span>
        <span className="text-slate-500 text-xs">{DATA.length}部屋</span>
      </div>

      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder="部屋番号・SSID・SB-ID・IPで検索..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 text-sm w-72"
        />
        <button
          onClick={() => setShowPw(v => !v)}
          className={`px-3 py-2 text-xs rounded-lg font-medium transition-colors ${showPw ? 'bg-red-800 text-red-200' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          {showPw ? '🔓 PW表示中' : '🔒 PW非表示'}
        </button>
        <span className="text-slate-500 text-xs">{filtered.length}件</span>
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
            {filtered.map((d, i) => (
              <tr key={d.room} className={`border-b border-slate-800 hover:bg-slate-800/50 ${i % 2 === 0 ? '' : 'bg-slate-900/30'}`}>
                <td className="py-2 px-3 font-bold text-white whitespace-nowrap">
                  {d.room === '玄関集合機' || d.room === '宅配ボックス'
                    ? <span className="px-2 py-0.5 bg-blue-900 text-blue-200 rounded text-xs">{d.room}</span>
                    : d.room
                  }
                </td>
                <td className="py-2 px-3 text-slate-300 font-mono text-xs whitespace-nowrap">{d.ap_ip}</td>
                <td className="py-2 px-3 text-slate-200 whitespace-nowrap">{d.ap_ssid}</td>
                <td className="py-2 px-3 font-mono text-xs whitespace-nowrap">
                  {showPw
                    ? <span className="text-green-300">{d.ap_wifi_pw}</span>
                    : <span className="text-slate-600">••••••••</span>
                  }
                </td>
                <td className="py-2 px-3 font-mono text-xs whitespace-nowrap">
                  {showPw
                    ? <span className="text-yellow-300">{d.ap_pw}</span>
                    : <span className="text-slate-600">••••••••</span>
                  }
                </td>
                <td className="py-2 px-3 text-slate-400 font-mono text-xs whitespace-nowrap">{d.ap_lan_mac}</td>
                <td className="py-2 px-3 text-slate-500 font-mono text-xs whitespace-nowrap">{d.ap_wan_mac}</td>
                <td className="py-2 px-3 whitespace-nowrap">
                  {d.sb_id
                    ? <span className="px-2 py-0.5 bg-slate-700 text-slate-200 rounded font-mono text-xs">{d.sb_id}</span>
                    : <span className="text-slate-600 text-xs">—</span>
                  }
                </td>
                <td className="py-2 px-3 text-slate-500 text-xs whitespace-nowrap">{d.sb_updated}</td>
                <td className="py-2 px-3 text-slate-600 text-xs whitespace-nowrap max-w-xs truncate">{d.ap_firmware}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
