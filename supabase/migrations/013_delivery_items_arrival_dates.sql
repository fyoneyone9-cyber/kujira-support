-- 機器ごとの「商品到着予定日」をダッシュボード側で管理できるようにする。
-- 例: { "P400": "2026-11-20", "PayCube": "2026-11-05" }
-- 到着予定日が入っていれば、リードタイムの推定値より優先して警告判定・理由文に使う。
alter table delivery_items add column if not exists equipment_arrival_dates jsonb default '{}'::jsonb;
