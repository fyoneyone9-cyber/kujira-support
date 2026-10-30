ALTER TABLE delivery_items
  ADD COLUMN IF NOT EXISTS p400_mtid text,
  ADD COLUMN IF NOT EXISTS p400_tid  text;
