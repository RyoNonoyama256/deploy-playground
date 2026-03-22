# deploy-playground

デプロイパターンの実験用ライブラリ

## 構成

| ディレクトリ | 内容 | デプロイ先 |
|---|---|---|
| `frontend-react/` | React + Vite 静的サイト | S3 + CloudFront |
| `frontend-next/` | Next.js SSR アプリ | Lambda / ECS（予定） |
| `backend/` | API サーバー | ECS / EC2（予定） |

## ワークフロー

| ファイル | トリガー | 内容 |
|---|---|---|
| `deploy-s3.yml` | 手動 | frontend-react → S3 + CloudFront |
