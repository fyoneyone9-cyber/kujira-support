create table if not exists purchase_orders (
  id uuid default gen_random_uuid() primary key,
  order_no text not null,
  order_date date not null,
  delivery_date text,
  vendor_name text not null default '日本コムネックス',
  vendor_zip text default '〒564-0052',
  vendor_address text default '大阪府吹田市岸部中10-40　TEK第1ビル5階',
  vendor_tel text default 'TEL：06-6338-1271　FAX：06-6338-5020',
  payment_terms text default '請求書払い',
  delivery_place text default '大阪府大阪市西区靭本町　本社',
  status text not null default 'draft',
  notes text,
  subtotal integer not null default 0,
  tax integer not null default 0,
  total integer not null default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists purchase_order_items (
  id uuid default gen_random_uuid() primary key,
  order_id uuid not null references purchase_orders(id) on delete cascade,
  sort_order integer not null default 0,
  description text not null,
  sub_description text,
  quantity integer not null default 1,
  unit text not null default '台',
  unit_price integer not null default 0,
  amount integer not null default 0,
  created_at timestamptz default now()
);

alter table purchase_orders enable row level security;
alter table purchase_order_items enable row level security;

create policy "auth users purchase_orders" on purchase_orders for all using (auth.role()='authenticated') with check (auth.role()='authenticated');
create policy "auth users purchase_order_items" on purchase_order_items for all using (auth.role()='authenticated') with check (auth.role()='authenticated');
