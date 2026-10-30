-- IoT製品 在庫管理テーブル（在庫切れ/残りわずか/更新古いアラート用）
create table if not exists inventory_items (
  id uuid default gen_random_uuid() primary key,
  part_no text,                                 -- 品番
  product_name text not null,                   -- 製品名
  stock integer default 0,                      -- 在庫
  incoming integer default 0,                   -- 入荷予定
  required integer default 0,                   -- 必要数
  diff integer default 0,                        -- 差分（在庫+入荷予定-必要数 等、CSVの差分列）
  notes text,                                    -- 備考
  last_stocktake_date date,                      -- 最終棚卸日（CSVヘッダ）
  row_hash text,                                 -- CSV行ハッシュ（重複判定）
  missing_in_last_import boolean default false,  -- 直近インポートに無かった
  acknowledged_at timestamptz,                   -- 在庫切れ等を確認済みにした日時
  imported_at timestamptz default now(),         -- このデータのインポート時刻（24hアラート判定）
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table inventory_items enable row level security;

-- 他テーブルと同様: authenticated / anon 両方許可（010_allow_anon_access 方針に合わせる）
create policy "authenticated all on inventory_items"
  on inventory_items for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

create policy "anon all on inventory_items"
  on inventory_items for all
  using (auth.role() = 'anon')
  with check (auth.role() = 'anon');

create trigger inventory_items_updated_at
  before update on inventory_items
  for each row execute function update_updated_at();

create index if not exists idx_inventory_items_product on inventory_items(product_name);
create index if not exists idx_inventory_items_imported on inventory_items(imported_at);
