-- SlackスレッドURL・HubSpot取引URLを手動でコピペして紐づけられるようにする。
alter table delivery_items add column if not exists slack_url text;
alter table delivery_items add column if not exists hubspot_url text;
