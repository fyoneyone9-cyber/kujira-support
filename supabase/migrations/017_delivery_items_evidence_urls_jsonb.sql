-- エビデンスURLを単一ではなく「項目名→URL」の複数管理に変更する。
-- 例: { "入金": "https://...", "PayCube": "https://...", "P400": "https://..." }
alter table delivery_items add column if not exists evidence_urls jsonb default '{}'::jsonb;
-- 旧 evidence_url（単一列）は使わないがデータ保護のため残す（削除しない）
