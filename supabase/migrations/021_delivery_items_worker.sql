-- 現地作業員の管理：必要/不要、作業日、作業員の連絡先（複数人想定でJSONB配列）
alter table delivery_items add column if not exists worker_needed boolean default false;
alter table delivery_items add column if not exists work_date date;
-- worker_contacts: [{ "name": "山田太郎", "tel": "090-xxxx-xxxx", "email": "x@x.com" }, ...]
alter table delivery_items add column if not exists worker_contacts jsonb default '[]'::jsonb;
