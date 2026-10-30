-- 案件を「固定（確定）」して誤編集を防げるようにする。
-- true=固定中（入力欄をreadonly化）、false/NULL=編集可能
alter table delivery_items add column if not exists locked boolean default false;
