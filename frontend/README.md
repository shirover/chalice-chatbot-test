# Chatbot Frontend (React)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build for production
- `npm run preview` - Preview the production build

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatContainer.tsx   # Main chat container
│   │   ├── MessageList.tsx     # Message display component
│   │   └── MessageInput.tsx    # Message input component
│   ├── hooks/
│   │   └── useChatbot.ts       # Custom hook for chat logic
│   ├── services/
│   │   └── chatService.ts      # API service
│   ├── styles/
│   │   └── *.css               # Component styles
│   ├── types/
│   │   └── chat.ts             # TypeScript interfaces
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Configuration

The frontend is configured to proxy API requests to the backend running on http://localhost:8000. This is configured in `vite.config.ts`.