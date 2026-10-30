-- 機器ごとの「納品予定日」をダッシュボード側で管理できるようにする。
-- 例: { "P400": "2026-11-20", "PayCube": "2026-11-05" }
-- 到着予定日（仕入先→自社）とは別に、機器単位で現地納品予定日を管理できるようにする。
alter table delivery_items add column if not exists equipment_delivery_dates jsonb default '{}'::jsonb;
