-- ホテル分析キャッシュテーブル（Gemini Google Search Grounding の課金削減）
create table if not exists hotel_analyze_cache (
  hotel_name text primary key,
  result jsonb not null,
  created_at timestamptz default now()
);

alter table hotel_analyze_cache enable row level security;

create policy "authenticated users can all on hotel_analyze_cache"
  on hotel_analyze_cache for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');
