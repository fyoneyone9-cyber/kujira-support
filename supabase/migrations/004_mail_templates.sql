-- メールテンプレートテーブル
create table if not exists mail_templates (
  id uuid default gen_random_uuid() primary key,
  category text not null,
  name text not null,
  purpose text,
  subject text,
  to_address text,
  cc_address text,
  body text,
  notes text,
  sort_order integer default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table mail_templates enable row level security;

create policy "authenticated users can all on mail_templates"
  on mail_templates for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

create index if not exists idx_mail_templates_category on mail_templates(category);
create index if not exists idx_mail_templates_sort on mail_templates(category, sort_order);
