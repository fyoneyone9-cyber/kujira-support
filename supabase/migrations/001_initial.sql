-- manuals テーブル
create table if not exists manuals (
  id uuid default gen_random_uuid() primary key,
  title text not null,
  category text,
  content text,
  created_by uuid references auth.users(id),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- RLS有効化
alter table manuals enable row level security;

-- 認証済みユーザーは読み取り可
create policy "authenticated users can read manuals"
  on manuals for select
  using (auth.role() = 'authenticated');

-- 認証済みユーザーは作成可
create policy "authenticated users can insert manuals"
  on manuals for insert
  with check (auth.role() = 'authenticated');

-- 認証済みユーザーは更新可
create policy "authenticated users can update manuals"
  on manuals for update
  using (auth.role() = 'authenticated');

-- 認証済みユーザーは削除可
create policy "authenticated users can delete manuals"
  on manuals for delete
  using (auth.role() = 'authenticated');
