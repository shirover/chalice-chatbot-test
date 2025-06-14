# チャットボットフロントエンド (React)

## セットアップ

1. 依存関係をインストール:
```bash
npm install
```

2. 開発サーバーを実行:
```bash
npm run dev
```

アプリケーションは http://localhost:3000 で利用可能になります

## 利用可能なスクリプト

- `npm run dev` - 開発サーバーを起動
- `npm run build` - プロダクション用にビルド
- `npm run preview` - プロダクションビルドをプレビュー

## プロジェクト構造

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatContainer.tsx   # メインチャットコンテナ
│   │   ├── MessageList.tsx     # メッセージ表示コンポーネント
│   │   └── MessageInput.tsx    # メッセージ入力コンポーネント
│   ├── hooks/
│   │   └── useChatbot.ts       # チャットロジック用カスタムフック
│   ├── services/
│   │   └── chatService.ts      # APIサービス
│   ├── styles/
│   │   └── *.css               # コンポーネントスタイル
│   ├── types/
│   │   └── chat.ts             # TypeScriptインターフェース
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 設定

フロントエンドは、http://localhost:8000で実行されているバックエンドへのAPIリクエストをプロキシするように設定されています。これは`vite.config.ts`で設定されています。