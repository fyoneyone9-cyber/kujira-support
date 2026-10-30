# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                    <div className="flex flex-col gap-2 min-w-fit">
                      <button
                        onClick={() => markChecked(it)}'''

new = '''                    <div className="flex flex-col gap-2 min-w-fit">
                      <a
                        href="https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        \U0001f6e0\ufe0f \u5de5\u7a0b\u7ba1\u7406\u8868
                      </a>
                      <a
                        href="https://docs.google.com/spreadsheets/d/1FxK4x534LV2sGY54KKtbow1W6iLT0Z_YTzg_R8ba8Go/edit?gid=0#gid=0"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        \U0001f4ca \u7ba1\u7406\u30b9\u30d7\u30ec\u30c3\u30c9\u30b7\u30fc\u30c8
                      </a>
                      <button
                        onClick={() => markChecked(it)}'''

if old in content:
    content = content.replace(old, new, 1)
    print('Buttons added OK')
else:
    print('ERROR: target not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
