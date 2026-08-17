-- PayCube保守契約テーブル
create table if not exists paycube_contracts (
  id uuid default gen_random_uuid() primary key,
  -- 設置先情報
  client_name text not null,                  -- 設置先名
  management_no text,                          -- 管理番号(コンラックス)
  management_no_dealer text,                   -- 管理番号(販売店)
  product_type text,                           -- 製品タイプ
  serial_no_hard text,                         -- 硬質ユニットシリアルNo.
  serial_no_bill text,                         -- 紙幣ユニットシリアルNo.
  -- 保守情報
  plan_name text,                              -- 保守サービス内容
  plan_type text default 'paid',               -- 'free'=無償 / 'paid'=有償
  start_date date,                             -- 保守開始日
  end_date date not null,                      -- 保守終了日
  -- ステータス
  status text default 'active',               -- 'active'/'alerted'/'contacted'/'renewed'/'expired'
  contacted_at timestamptz,                    -- 顧客への連絡日時
  renewed_at timestamptz,                      -- 更新完了日時
  notes text,                                  -- 備考
  -- メタ
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- RLS有効化
alter table paycube_contracts enable row level security;

-- 認証済みユーザーは全操作可
create policy "authenticated users can all on paycube_contracts"
  on paycube_contracts for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

-- updated_at 自動更新トリガー
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger paycube_contracts_updated_at
  before update on paycube_contracts
  for each row execute function update_updated_at();

-- インデックス
create index if not exists idx_paycube_contracts_end_date on paycube_contracts(end_date);
create index if not exists idx_paycube_contracts_status on paycube_contracts(status);
