-- slack_logs テーブル
create table if not exists slack_logs (
  id uuid default gen_random_uuid() primary key,
  title text,
  content text not null,
  created_by uuid references auth.users(id),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table slack_logs enable row level security;

create policy "auth_read" on slack_logs for select using (auth.role() = 'authenticated');
create policy "auth_insert" on slack_logs for insert with check (auth.role() = 'authenticated');
create policy "auth_update" on slack_logs for update using (auth.role() = 'authenticated');
create policy "auth_delete" on slack_logs for delete using (auth.role() = 'authenticated');
