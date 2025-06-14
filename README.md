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
- Rate limiting to prevent API abuse
- Request body size limits (1MB)
- Security headers (CSP, HSTS, etc.)
- HTTPS/SSL support for production

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

#### Basic HTTP Deployment

1. **Update environment variables**:
   - Set `EC2_PUBLIC_IP` in `.env`
   - Set `PRODUCTION_FRONTEND_URL` if using a domain
   - Configure `AWS_REGION` if needed

2. **Security Group Configuration**:
   - Port 80 (HTTP) for frontend
   - Port 443 (HTTPS) for frontend (if using SSL)
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
   
   # Build and run (HTTP)
   docker-compose up -d --build
   ```

#### HTTPS/SSL Deployment

1. **Obtain SSL Certificates**:
   ```bash
   # Using Let's Encrypt (recommended)
   sudo apt-get update
   sudo apt-get install certbot
   
   # Generate certificates
   sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
   
   # Certificates will be in:
   # /etc/letsencrypt/live/yourdomain.com/fullchain.pem (cert.pem)
   # /etc/letsencrypt/live/yourdomain.com/privkey.pem (key.pem)
   ```

2. **Prepare SSL Certificates**:
   ```bash
   # Create SSL directory
   mkdir -p ssl
   
   # Copy certificates (or create symlinks)
   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
   sudo chmod 644 ssl/cert.pem
   sudo chmod 600 ssl/key.pem
   ```

3. **Deploy with HTTPS**:
   ```bash
   # Use production docker-compose with SSL
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

4. **Auto-renew SSL Certificates**:
   ```bash
   # Add to crontab
   sudo crontab -e
   
   # Add this line to renew certificates automatically
   0 2 * * * certbot renew --quiet && docker-compose -f docker-compose.prod.yml restart frontend
   ```

#### Using AWS Application Load Balancer (ALB)

For production deployments, consider using AWS ALB for SSL termination:

1. Create an ALB with HTTPS listener
2. Configure SSL certificate in AWS Certificate Manager
3. Point ALB to EC2 instance on port 80
4. Update security groups accordingly
5. Use standard `docker-compose.yml` (ALB handles SSL)

### Environment Variables

Key environment variables for production:

- `ENVIRONMENT`: Set to "production"
- `EC2_PUBLIC_IP`: Your EC2 instance public IP
- `PRODUCTION_FRONTEND_URL`: Your domain URL (if applicable)
- `RATE_LIMIT_PER_MINUTE`: API rate limiting (default: 60)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins
- `AWS_REGION`: AWS region for future AWS service integrations

### Security Considerations

#### Implemented Security Features

1. **Input Validation**:
   - Message length limits (1-1000 characters)
   - Request body size limit (1MB)
   - Whitespace and empty message validation

2. **Rate Limiting**:
   - Configurable per-minute request limits
   - Per-IP address tracking

3. **Security Headers**:
   - Content Security Policy (CSP)
   - Strict Transport Security (HSTS) for HTTPS
   - X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
   - Referrer Policy

4. **CORS Protection**:
   - Whitelist-based origin validation
   - Specific method and header restrictions

5. **Error Handling**:
   - Generic error messages to prevent information leakage
   - Proper logging without exposing sensitive data

#### Additional Security Recommendations

1. **Authentication**: Implement JWT or session-based authentication
2. **API Keys**: Use AWS Secrets Manager for sensitive configuration
3. **Monitoring**: Set up CloudWatch alerts for suspicious activity
4. **WAF**: Consider AWS WAF for additional protection
5. **Updates**: Regularly update dependencies and Docker images

## License

This project is open source and available under the MIT License.