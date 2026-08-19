-- 引き当てルールテーブル
create table if not exists assignment_rules (
  id uuid default gen_random_uuid() primary key,
  keyword text not null,           -- メール件名・内容のキーワード
  assignee text not null,          -- 担当者名
  assignee_email text,             -- 担当者メールアドレス
  action text,                     -- 対応方法（引き当て/対応完了/Slack報告等）
  notes text,                      -- 備考
  priority integer default 0,      -- 優先度（！マーク=重要=高い数値）
  is_active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table assignment_rules enable row level security;

create policy "authenticated users can all on assignment_rules"
  on assignment_rules for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

create index if not exists idx_assignment_rules_keyword on assignment_rules using gin(to_tsvector('simple', keyword));
create index if not exists idx_assignment_rules_assignee on assignment_rules(assignee);
create index if not exists idx_assignment_rules_priority on assignment_rules(priority desc);
