-- dashboard_todos: チェックボックス・メモ等のUI状態を格納するJSONBカラム
ALTER TABLE delivery_items
  ADD COLUMN IF NOT EXISTS dashboard_todos jsonb DEFAULT '{}'::jsonb,
  ADD COLUMN IF NOT EXISTS dashboard_memo  text;
