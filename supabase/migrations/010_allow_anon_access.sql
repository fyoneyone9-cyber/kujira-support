-- 010_allow_anon_access.sql
-- 完全ローカル動作(ログイン認証なし)構成のため、全テーブルでanon(匿名)ロールにも
-- フルアクセスを許可する。authenticated限定ポリシーのままだと、ログインしていない
-- 現在の運用では常に空配列が返り、全機能が『読み込み中のまま止まる』状態になっていた。
-- (このアプリは社内ローカル専用で外部公開しない前提)
-- テーブルが存在しない環境でもエラーにならないよう、存在確認してから処理する。

do $$
declare
  t text;
  tables text[] := array['manuals','slack_logs','paycube_contracts','mail_templates',
                          'assignment_rules','hotel_analyze_cache','purchase_orders',
                          'purchase_order_items','p400_orders','delivery_items'];
begin
  foreach t in array tables loop
    if to_regclass(t) is not null then
      -- 既存のauthenticated限定ポリシーを全部落とす(名前がどうであれ)
      execute (
        select coalesce(string_agg(format('drop policy if exists %I on %I;', policyname, t), ' '), '')
        from pg_policies where schemaname = 'public' and tablename = t
      );
      execute format('create policy %I on %I for all using (true) with check (true);',
                      'anon can all on ' || t, t);
      raise notice 'OK: % policy updated', t;
    else
      raise notice 'SKIP: table % does not exist', t;
    end if;
  end loop;
end $$;
