-- 入金あり/なしのチェック状態をダッシュボード側で管理する。
-- true=入金確認済み, false/NULL=未確認
alter table delivery_items add column if not exists payment_received boolean default false;
