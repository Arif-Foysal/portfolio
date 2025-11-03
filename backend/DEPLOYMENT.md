# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

## Deployment Steps

### 1. Environment Variables
Set up your environment variables in Vercel dashboard or CLI:

```bash
vercel env add SUPABASE_URL production
vercel env add SUPABASE_KEY production
```

Or add them in the Vercel dashboard:
- Go to your project settings
- Navigate to Environment Variables
- Add:
  - `SUPABASE_URL`: Your Supabase project URL
  - `SUPABASE_KEY`: Your Supabase anon key

### 2. Deploy

From the backend directory, run:
```bash
cd backend
vercel --prod
```

Or for preview deployment:
```bash
vercel
```

### 3. Project Structure for Vercel

```
backend/
├── api/
│   └── index.py         # Vercel entry point
├── routes/
│   ├── __init__.py
│   ├── main.py
│   └── newsletter.py
├── config.py
├── database.py
├── models.py
├── main.py             # Main FastAPI app
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
└── .vercelignore      # Files to ignore during deployment
```

## API Endpoints

Once deployed, your API will be available at:
- `https://your-app.vercel.app/` - Welcome message
- `https://your-app.vercel.app/health` - Health check
- `https://your-app.vercel.app/newsletter/subscribe` - Newsletter subscription
- `https://your-app.vercel.app/docs` - Swagger documentation

## Environment Variables Required

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/public key

## Troubleshooting

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Environment Variables**: Ensure they're set in Vercel dashboard
3. **CORS Issues**: Add CORS middleware if needed for frontend integration
4. **Cold Starts**: First request might be slower due to serverless nature

## Local Testing

Test locally before deploying:
```bash
cd backend
pip install -r requirements.txt
python main.py
```

Visit `http://localhost:8000/docs` to test the API.
