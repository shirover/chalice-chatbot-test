# チャットボットアプリケーション

React（フロントエンド）とFastAPI（バックエンド）で構築されたモダンなチャットボットアプリケーション。

## プロジェクト構造

```
.
├── backend/           # FastAPIバックエンド
│   ├── app/
│   │   ├── api/      # APIエンドポイント
│   │   ├── core/     # コア設定
│   │   ├── services/ # ビジネスロジック
│   │   └── main.py   # FastAPIアプリケーション
│   └── requirements.txt
├── frontend/          # Reactフロントエンド
│   ├── src/
│   │   ├── components/  # Reactコンポーネント
│   │   ├── hooks/       # カスタムフック
│   │   ├── services/    # APIサービス
│   │   ├── styles/      # CSSスタイル
│   │   └── types/       # TypeScript型定義
│   └── package.json
└── README.md
```

## クイックスタート

### バックエンドのセットアップ

1. バックエンドディレクトリに移動:
```bash
cd backend
```

2. 仮想環境を作成して有効化:
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

3. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

4. `.env.example`を`.env`にコピーして必要に応じて設定。

5. 開発サーバーを実行:
```bash
uvicorn app.main:app --reload
```

APIは http://localhost:8000 で利用可能になります

### フロントエンドのセットアップ

1. フロントエンドディレクトリに移動:
```bash
cd frontend
```

2. 依存関係をインストール:
```bash
npm install
```

3. 開発サーバーを実行:
```bash
npm run dev
```

アプリケーションは http://localhost:3000 で利用可能になります

## 機能

- リアルタイムチャットインターフェース
- FastAPIによるRESTful API
- TypeScriptを使用したReact
- モジュラーで拡張可能なアーキテクチャ
- 開発用のCORS設定
- 自動スクロールメッセージリスト
- ローディング状態とエラーハンドリング

## カスタマイズ

### 新機能の追加

1. **バックエンド**: `backend/app/api/endpoints/`に新しいエンドポイントを追加
2. **フロントエンド**: `frontend/src/components/`に新しいコンポーネントを追加
3. **サービス**: `backend/app/services/`にビジネスロジックを実装
4. **スタイリング**: `frontend/src/styles/`でスタイルをカスタマイズ

### AIモデルの統合

実際のAIモデル（例：OpenAI、Anthropic、カスタムモデル）を統合するには：

1. `backend/app/services/chatbot.py`をAI統合で更新
2. 必要なAPIキーを`.env`ファイルに追加
3. 必要なPythonパッケージをインストールし、`requirements.txt`を更新

## 開発

- バックエンドAPIドキュメント: http://localhost:8000/docs
- フロントエンド開発サーバー: http://localhost:3000
- フロントエンドとバックエンドの両方でホットリロードが有効

## ライセンス

このプロジェクトはオープンソースで、MITライセンスの下で利用可能です。