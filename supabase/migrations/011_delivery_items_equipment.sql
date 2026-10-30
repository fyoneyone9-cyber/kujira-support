-- IoT機器の内訳（CSVのPMS/カードキー/キーボックス/P400/PayCube/VEGA3000等の列）と
-- 長納期機器の手配状況列を取り込めるようにする。
-- これにより「どの機器が原因で遅延リスクがあるか」をアラート文で具体的に案内できる。

alter table delivery_items add column if not exists equipment jsonb default '[]'::jsonb;
alter table delivery_items add column if not exists p400_status text;
alter table delivery_items add column if not exists paycube_status text;
alter table delivery_items add column if not exists vega3000_status text;

comment on column delivery_items.equipment is
  'CSVの機器列（PMS/カードディスペンサー/カードキー種類/キーボックス/スマートロック/PayCube/VEGA3000/P400/パスポートリーダー/Surface周辺機器/卓上QR/雨除けカバー/タブレットスタンド等）のうち「--」「空」以外が入っていたものを [{name, value}] の配列で保存';
