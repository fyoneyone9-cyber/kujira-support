sql = """
-- カラムが既に存在する場合はデフォルト値をNULLに変更
ALTER TABLE delivery_items
  ALTER COLUMN pms_linked SET DEFAULT NULL,
  ALTER COLUMN pms_linked DROP NOT NULL;

ALTER TABLE delivery_items
  ALTER COLUMN smartlock_linked SET DEFAULT NULL,
  ALTER COLUMN smartlock_linked DROP NOT NULL;

-- 既存行でfalse（不要）になっているものをNULL（未連携）に戻す
UPDATE delivery_items
  SET pms_linked = NULL
  WHERE pms_linked = false;

UPDATE delivery_items
  SET smartlock_linked = NULL
  WHERE smartlock_linked = false;
"""
print("=== Supabase SQLエディタで実行してください ===")
print(sql)
print("URL: https://supabase.com/dashboard/project/fjkpdejyusnttbhdmyxt/sql/new")
