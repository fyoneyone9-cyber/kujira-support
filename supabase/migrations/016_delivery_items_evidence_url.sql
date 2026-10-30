-- 発注・納品・入金などのエビデンス（証憑）URL（Driveリンク等）を保存できるようにする。
alter table delivery_items add column if not exists evidence_url text;
