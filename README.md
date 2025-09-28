# iNFT Agent Backend

A FastAPI-based backend service for managing Interactive Non-Fungible Tokens (iNFTs) with AI-powered chat capabilities and semantic search functionality.

## Features

- **iNFT Management**: Create, store, and manage iNFTs with metadata and traits
- **AI-Powered Chat**: Interactive chat functionality with each iNFT using ASI API
- **Semantic Search**: Vector-based similarity search using sentence transformers and FAISS
- **Feedback System**: Rating and feedback mechanism for iNFTs with score computation
- **Web3 Storage**: Mock Web3 storage integration for file management
- **SQLite Database**: Persistent storage for iNFTs and feedback data

##  Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **AI/ML**: 
  - ASI API for chat completions
  - Sentence Transformers (all-MiniLM-L6-v2) for embeddings
  - FAISS for vector similarity search
- **Dependencies**: 
  - `uvicorn` - ASGI server
  - `python-dotenv` - Environment variable management
  - `requests` - HTTP client
  - `pydantic` - Data validation

##  Project Structure

```
Backend/
├── __init__.py          # Package initialization
├── main.py             # FastAPI application entry point
├── config.py           # Configuration and environment variables
├── db.py              # Database initialization and schema
├── routes.py          # API endpoints and route handlers
├── utils.py           # Utility functions (Web3 storage, ASI API calls)
└── embedding.py       # Vector embeddings and semantic search
```

##  Configuration

Create a `.env` file in the root directory with the following variables:

```env
ASI_API_KEY=your_asi_api_key_here
ASI_MODEL=asi1-mini
```

##  Database Schema

### iNFTs Table
- `id`: Primary key (auto-increment)
- `name`: iNFT name
- `owner`: Owner address/identifier
- `tag`: Category/tag
- `cid`: Content identifier (Web3 storage)
- `traits_json`: JSON string of traits/metadata
- `score`: Average rating score (0-10)
- `created_at`: Timestamp

### Feedbacks Table
- `id`: Primary key (auto-increment)
- `inft_id`: Reference to iNFT
- `rating`: Rating score (0-10)
- `comment`: Optional feedback comment
- `created_at`: Timestamp

##  API Endpoints

### iNFT Management
- `POST /create_inft` - Create a new iNFT with metadata
- `GET /list_infts` - List all iNFTs with their details

### Chat & Interaction
- `POST /chat/{inft_id}` - Chat with a specific iNFT using AI

### Feedback System
- `POST /feedback/{inft_id}` - Submit rating and feedback for an iNFT

##  AI Features

### Chat System
- Each iNFT has a unique persona based on its name, tag, and traits
- Uses ASI API for generating contextual responses
- Incorporates relevant memory through semantic search

### Semantic Search
- Converts text data into vector embeddings using sentence transformers
- Stores embeddings in FAISS index for fast similarity search
- Retrieves relevant context for chat interactions

##  Core Workflows

1. **iNFT Creation**: 
   - Store metadata in database
   - Generate embeddings from traits
   - Mock upload to Web3 storage

2. **Chat Interaction**:
   - Retrieve iNFT persona and traits
   - Search for relevant memories using embeddings
   - Generate AI response with context

3. **Feedback Processing**:
   - Store user feedback
   - Recompute average score
   - Update iNFT rating

##  Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create `.env` file with ASI API credentials

3. **Run the Server**:
   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

4. **Access API Documentation**:
   Visit `http://localhost:8000/docs` for interactive API documentation

## Security Features

- CORS middleware configured for cross-origin requests
- Input validation using Pydantic models
- Error handling for API failures
- SQLite connection with thread safety

##  Performance Optimizations

- In-memory FAISS index for fast vector search
- Connection pooling for database operations
- Efficient embedding generation and storage
- Mock Web3 storage for development/testing

##  Development Notes

- Uses mock Web3 storage implementation for development
- Fallback mock responses when ASI API is unavailable
- Thread-safe database operations
- Comprehensive error handling and HTTP status codes

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the iNFT Agent ecosystem for creating interactive and intelligent NFTs with AI capabilities.
