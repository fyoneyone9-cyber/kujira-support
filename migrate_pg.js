const { Client } = require('pg');

// Supabase direct DB connection
// Format: postgresql://postgres.[project-ref]:[password]@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres
// We need the DB password - try with service_role JWT as password (sometimes works)
const serviceKey = process.env.SERVICE_KEY;
const projectRef = 'fjkpdejyusnttbhdmyxt';

// Transaction pooler connection
const connectionString = `postgresql://postgres.${projectRef}:${serviceKey}@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres`;

const client = new Client({ connectionString, ssl: { rejectUnauthorized: false } });

const sql = `
CREATE TABLE IF NOT EXISTS manuals (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  category text,
  content text,
  created_by uuid,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
ALTER TABLE manuals ENABLE ROW LEVEL SECURITY;
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='manuals' AND policyname='auth_read') THEN
    CREATE POLICY "auth_read" ON manuals FOR SELECT USING (auth.role() = 'authenticated');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='manuals' AND policyname='auth_insert') THEN
    CREATE POLICY "auth_insert" ON manuals FOR INSERT WITH CHECK (auth.role() = 'authenticated');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='manuals' AND policyname='auth_update') THEN
    CREATE POLICY "auth_update" ON manuals FOR UPDATE USING (auth.role() = 'authenticated');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='manuals' AND policyname='auth_delete') THEN
    CREATE POLICY "auth_delete" ON manuals FOR DELETE USING (auth.role() = 'authenticated');
  END IF;
END $$;
`;

async function main() {
  try {
    await client.connect();
    console.log('Connected!');
    await client.query(sql);
    console.log('Migration completed!');
  } catch (e) {
    console.error('Error:', e.message);
  } finally {
    await client.end();
  }
}
main();
