create table if not exists p400_orders (
  id uuid default gen_random_uuid() primary key,
  order_no text not null,
  order_date date not null,
  store_name text not null,
  store_address text,
  store_tel text,
  store_manager text,
  general_manager text,
  delivery_place text,
  payment_terms text default '別途請求',
  notes text,
  qty_p400 integer not null default 0,
  qty_setup_credit integer not null default 0,
  qty_setup_emoney integer not null default 0,
  qty_setup_qr integer not null default 0,
  qty_cable integer not null default 0,
  subtotal integer not null default 0,
  tax integer not null default 0,
  total integer not null default 0,
  status text not null default 'draft',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table p400_orders enable row level security;
create policy "auth users p400_orders" on p400_orders for all using (auth.role()='authenticated') with check (auth.role()='authenticated');
