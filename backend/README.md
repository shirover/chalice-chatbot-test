# チャットボットバックエンド (FastAPI)

## セットアップ

1. 仮想環境を作成:
```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

3. `.env.example`を`.env`にコピーして、必要に応じて値を更新。

4. 開発サーバーを実行:
```bash
uvicorn app.main:app --reload
```

APIは http://localhost:8000 で利用可能になります

## APIドキュメント

サーバーが起動したら、以下にアクセスできます：
- インタラクティブAPIドキュメント: http://localhost:8000/docs
- 代替APIドキュメント: http://localhost:8000/redoc

## プロジェクト構造

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── chat.py      # チャットエンドポイント
│   ├── core/
│   │   └── config.py        # 設定
│   ├── services/
│   │   └── chatbot.py       # チャットボットサービスロジック
│   └── main.py              # FastAPIアプリケーション
├── requirements.txt
└── .env.example
```