# 🐋 KUJIRA サポートシステム

導入支援チーム向けの内部業務システムです。

## 機能

- 🔐 招待制ログイン（Supabase Auth / マジックリンク）
- 📋 マニュアル管理（作成・編集・検索）
- ⚡ 自動化管理（準備中）
- 👥 メンバー招待管理

## セットアップ

### 1. 依存パッケージのインストール

```bash
npm install
```

### 2. Supabaseプロジェクトを作成

https://supabase.com/dashboard でプロジェクトを新規作成

### 3. DBマイグレーション実行

Supabase SQL エディタで `supabase/migrations/001_initial.sql` の内容を実行

### 4. 環境変数の設定

`.env.local.example` をコピーして `.env.local` を作成し、値を設定：

```bash
cp .env.local.example .env.local
```

```
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 5. ローカル起動

```bash
npm run dev
```

http://localhost:3000 でアクセス

## Vercelデプロイ

1. GitHubリポジトリと連携
2. 環境変数を Vercel の Settings > Environment Variables に設定
3. デプロイ後 `support.nextralab.jp` のDNS設定（CNAME → vercel）

## SupabaseのAuth設定

Supabase Dashboard > Authentication > URL Configuration で
- Site URL: `https://support.nextralab.jp`
- Redirect URLs に `https://support.nextralab.jp/auth/callback` を追加

## 技術スタック

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Supabase (Auth + PostgreSQL)
- Vercel
