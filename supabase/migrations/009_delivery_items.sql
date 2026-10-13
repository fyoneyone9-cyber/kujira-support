-- IoT製品納品管理テーブル（納品予定日アラート用）
create table if not exists delivery_items (
  id uuid default gen_random_uuid() primary key,
  -- 案件情報
  client_name text not null,                   -- 企業名
  install_address text,                        -- 設置先住所
  product_name text,                           -- 製品名
  quantity integer,                             -- 台数
  progress text,                                -- 進捗（動作確認待ち/未着手/キッティング中/入荷待ち/出荷待ち等）
  assignee text,                                -- 担当
  -- 日付
  delivery_due_date date,                       -- 納品予定日
  delivery_date date,                           -- 納品日（入っていれば完了扱い）
  -- 連絡先
  contact_name text,                            -- 担当者名
  contact_tel1 text,                            -- 担当連絡先①
  contact_tel2 text,                            -- 担当連絡先②
  notes text,                                   -- 備考
  -- ステータス
  status text default 'active',                 -- 'active'/'done'/'alerted'
  acknowledged_at timestamptz,                  -- 確認済みにした日時
  -- メタ
  row_hash text,                                -- CSV行の内容ハッシュ（重複判定用）
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- RLS有効化
alter table delivery_items enable row level security;

create policy "authenticated users can all on delivery_items"
  on delivery_items for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

create trigger delivery_items_updated_at
  before update on delivery_items
  for each row execute function update_updated_at();

create index if not exists idx_delivery_items_due_date on delivery_items(delivery_due_date);
create index if not exists idx_delivery_items_status on delivery_items(status);
