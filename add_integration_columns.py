import urllib.request, json

# Supabase REST APIでALTER TABLEは実行できないのでSQLを表示するだけ
sql = """
ALTER TABLE delivery_items
  ADD COLUMN IF NOT EXISTS pms_linked boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS smartlock_linked boolean DEFAULT false;
"""
print("=== Supabase SQLエディタで実行してください ===")
print(sql)
print("URL: https://supabase.com/dashboard/project/fjkpdejyusnttbhdmyxt/sql/new")
