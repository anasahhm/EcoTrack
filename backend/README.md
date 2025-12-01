# EcoTrack Backend API

FastAPI backend for EcoTrack Environmental Impact Analyzer.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-change-in-production
```

3. Run development server:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
```

---



