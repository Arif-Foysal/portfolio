# Portfolio Backend

A modular FastAPI backend for portfolio website with newsletter subscription functionality.

## Project Structure

```
backend/
├── main.py              # Application entry point
├── config.py            # Configuration and settings
├── database.py          # Database connection and operations
├── models.py            # Pydantic models
├── routes/              # API route modules
│   ├── __init__.py
│   ├── main.py          # General routes (welcome, health)
│   └── newsletter.py    # Newsletter subscription routes
├── .env                 # Environment variables (not tracked)
├── pyproject.toml       # Project dependencies
└── README.md            # This file
```

## Features

- **Modular Architecture**: Separated concerns into different modules
- **Environment Configuration**: Centralized settings management
- **Database Integration**: Supabase integration with graceful fallback
- **Email Validation**: Pydantic EmailStr validation
- **Error Handling**: Comprehensive error handling and logging
- **Health Checks**: Built-in health check endpoint

## API Endpoints

### General
- `GET /` - Welcome message
- `GET /health` - Health check

### Newsletter
- `POST /newsletter/subscribe` - Subscribe to newsletter
  - Body: `{"email": "user@example.com", "name": "Optional Name"}`

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Server Configuration (optional)
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## Database Schema

Create a table named `newsletter_subscribers` in Supabase:

```sql
CREATE TABLE newsletter_subscribers (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Running the Application

```bash
# Install dependencies
uv sync

# Run the application
uv run main.py
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic[email]` - Data validation with email support
- `python-dotenv` - Environment variable loading
- `supabase` - Database client
