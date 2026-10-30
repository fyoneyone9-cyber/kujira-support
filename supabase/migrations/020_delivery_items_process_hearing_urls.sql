-- 案件ごとの工程管理表（該当シート行など）・ヒアリングシートのURLを手動で登録できるようにする。
alter table delivery_items add column if not exists process_sheet_url text;
alter table delivery_items add column if not exists hearing_sheet_url text;
