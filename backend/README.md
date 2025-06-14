# Chatbot Backend (FastAPI)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update the values as needed.

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access:
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── chat.py      # Chat endpoints
│   ├── core/
│   │   └── config.py        # Configuration settings
│   ├── services/
│   │   └── chatbot.py       # Chatbot service logic
│   └── main.py              # FastAPI application
├── requirements.txt
└── .env.example
```