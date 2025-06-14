# Chatbot Application

A modern chatbot application built with React (frontend) and FastAPI (backend).

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core configuration
│   │   ├── services/ # Business logic
│   │   └── main.py   # FastAPI application
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API services
│   │   ├── styles/      # CSS styles
│   │   └── types/       # TypeScript types
│   └── package.json
└── README.md
```

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure as needed.

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Features

- Real-time chat interface
- RESTful API with FastAPI
- React with TypeScript
- Modular and extensible architecture
- CORS configuration for development
- Auto-scrolling message list
- Loading states and error handling

## Customization

### Adding New Features

1. **Backend**: Add new endpoints in `backend/app/api/endpoints/`
2. **Frontend**: Add new components in `frontend/src/components/`
3. **Services**: Implement business logic in `backend/app/services/`
4. **Styling**: Customize styles in `frontend/src/styles/`

### Integrating AI Models

To integrate actual AI models (e.g., OpenAI, Anthropic, or custom models):

1. Update `backend/app/services/chatbot.py` with your AI integration
2. Add necessary API keys to the `.env` file
3. Install required Python packages and update `requirements.txt`

## Development

- Backend API documentation: http://localhost:8000/docs
- Frontend development server: http://localhost:3000
- Hot-reloading enabled for both frontend and backend

## License

This project is open source and available under the MIT License.