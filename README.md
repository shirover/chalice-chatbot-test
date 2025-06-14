# Chatbot Application

A modern chatbot application built with React (frontend) and FastAPI (backend), designed for both local development and AWS EC2 deployment.

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

The application will be available at http://localhost:5173

## Features

- Real-time chat interface with message validation
- RESTful API with FastAPI and input validation
- React with TypeScript and proper error handling
- Modular and extensible architecture
- CORS configuration for development and production
- Auto-scrolling message list with message limits
- Loading states and error handling
- Request cancellation support
- Docker support for easy deployment
- AWS EC2 deployment ready
- Comprehensive test structure

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

### Local Development

- Backend API documentation: http://localhost:8000/docs
- Frontend development server: http://localhost:5173
- Hot-reloading enabled for both frontend and backend

### Docker Development

```bash
# Run with Docker Compose (development)
docker-compose -f docker-compose.dev.yml up

# Run with Docker Compose (production)
docker-compose up --build
```

### Testing

#### Backend Tests
```bash
cd backend
pytest
# With coverage
pytest --cov=app
```

#### Frontend Tests
```bash
cd frontend
npm test
# With coverage
npm run test:coverage
```

## Deployment

### AWS EC2 Deployment

1. **Update environment variables**:
   - Set `EC2_PUBLIC_IP` in `.env`
   - Set `PRODUCTION_FRONTEND_URL` if using a domain
   - Configure `AWS_REGION` if needed

2. **Security Group Configuration**:
   - Port 80 (HTTP) for frontend
   - Port 8000 (or custom) for backend API
   - Port 22 (SSH) for administration

3. **Deploy with Docker**:
   ```bash
   # On EC2 instance
   git clone <your-repo>
   cd <your-repo>
   
   # Copy and configure .env files
   cp backend/.env.example backend/.env
   # Edit backend/.env with production values
   
   # Build and run
   docker-compose up -d --build
   ```

4. **Configure Nginx (optional)**:
   - Use the provided `frontend/nginx.conf` as a reference
   - Set up SSL with Let's Encrypt for HTTPS

### Environment Variables

Key environment variables for production:

- `ENVIRONMENT`: Set to "production"
- `EC2_PUBLIC_IP`: Your EC2 instance public IP
- `PRODUCTION_FRONTEND_URL`: Your domain URL (if applicable)
- `RATE_LIMIT_PER_MINUTE`: API rate limiting
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## License

This project is open source and available under the MIT License.