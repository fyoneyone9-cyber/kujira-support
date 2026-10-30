-- 長納期機器（P400/PayCube/VEGA3000）の手配状況カラムを追加
-- CSV側の「P400 手配状況」「PayCube 手配状況」「VEGA3000 手配状況」列を取り込み、
-- アラート理由文で「発注済みかどうか」を具体的に案内できるようにする。
alter table delivery_items add column if not exists p400_status text;
alter table delivery_items add column if not exists paycube_status text;
alter table delivery_items add column if not exists vega3000_status text;
