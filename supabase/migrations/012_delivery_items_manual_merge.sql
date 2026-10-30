-- CSVを都度まるごと再取込しても、ダッシュボード側で入力した内容が消えないようにする。
--
-- 方針：
--  ・item_key（会社名＋設置先住所＋製品名から生成する安定キー）で行を一意に特定し、
--    再取込時は「削除してから全挿入」ではなく「upsert」に変更する。
--  ・CSV由来の列（住所・製品名・台数・進捗・担当・納期・連絡先・機器内訳・手配状況メモ等）は
--    毎回CSVの内容で上書きする。
--  ・ダッシュボード側でしか入力しない列（手動発注チェック・メモ・確認者/確認日時・既読状態）は
--    import処理では一切触らないので、再取込しても保持される。

alter table delivery_items add column if not exists item_key text;
create unique index if not exists idx_delivery_items_item_key on delivery_items(item_key);

-- ダッシュボード側で「発注した」とチェックした機器（P400/PayCube/VEGA3000等、複数ありうる）
alter table delivery_items add column if not exists manual_ordered jsonb default '[]'::jsonb;

-- ダッシュボード側の自由メモ（CSVのnotesとは別に、担当者が気づいたことを書き込む用）
alter table delivery_items add column if not exists dashboard_memo text;

-- 「内容を確認した」ことの記録（納品完了にはしないが、見た・把握したという印）
alter table delivery_items add column if not exists checked_by text;
alter table delivery_items add column if not exists checked_at timestamptz;

-- 直近の取込でCSVに存在しなくなった行を検知するためのフラグ
alter table delivery_items add column if not exists missing_in_last_import boolean default false;
alter table delivery_items add column if not exists last_imported_at timestamptz;
