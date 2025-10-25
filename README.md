# Smart-Housing - AI-Powered House Price Prediction Platform

A Django web application that predicts house prices using machine learning and automatically retrains models with fresh data. Features a responsive design, real-time predictions, and production-ready deployment configuration.

![Project Demo](assets/demo.gif)

## Features

- **AI-Powered Predictions**: Accurate house price estimates using machine learning
- **Real-Time Processing**: Instant predictions with a single click
- **Auto-Retraining**: Models automatically retrain every 24 hours using fresh data
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Production Ready**: Configured for Railway deployment with proper security settings

### Prediction Features
- Input form with comprehensive property details:
  - House size (square feet)
  - Number of bedrooms
  - House age (years)
  - Location (Downtown, Suburbs, Rural)
  - House type (Villa, Apartment, L-shape, Normal)
- One-hot encoding for categorical variables
- Model artifacts saved to `checkpoints/`:
  - `model_latest.joblib`
  - `scaler.joblib`

## Project Structure

```
smart-housing/
├── prediction/                 # Django project
│   ├── prediction/            # Project settings
│   │   ├── settings.py        # Production-ready configuration
│   │   ├── urls.py           # URL routing
│   │   └── wsgi.py           # WSGI application
│   └── predict/              # Main Django app
│       ├── templates/         # HTML templates
│       │   ├── base.html     # Responsive base template
│       │   ├── home.html     # Landing page
│       │   ├── predict.html  # Prediction form
│       │   ├── about.html    # About page
│       │   └── contact.html  # Contact form
│       ├── static/           # Static files (CSS, JS, images)
│       ├── views.py         # View functions
│       ├── urls.py          # App URL patterns
│       ├── ml_model.py      # ML prediction logic
│       └── tasks.py         # Celery tasks
├── assets/                   # Repository-level assets
├── checkpoints/             # Saved ML models
├── data/                   # Training data
├── scripts/                # Data generation scripts
├── Procfile               # Railway deployment
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version
└── README.md            # This file
```

## Technology Stack

- **Backend**: Django 5.2.6, Python 3.11
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Task Queue**: Celery with Redis
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway, Gunicorn, WhiteNoise
- **Database**: SQLite (development), PostgreSQL (production ready)

## Quick Start (Development)

1. **Clone the repository and set up environment**
```bash
git clone <repository-url>
cd smart-housing
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start Redis (required for Celery)**
```bash
# Using Docker (recommended)
docker run --name redis -p 6379:6379 -d redis:7

# Or install Redis locally
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Linux/Mac: brew install redis && redis-server
```

3. **Generate training data**
```bash
python scripts/data_generator.py
```

4. **Run Django development server**
```bash
cd prediction
python manage.py runserver
```

5. **Run Celery worker and Beat (separate terminals)**
```bash
cd prediction
celery -A prediction worker -l info
celery -A prediction beat -l info
```

6. **Access the application**
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Railway Deployment

### One-Line Deployment Checklist
1. Create Railway project → Connect GitHub repo → Add environment variables → Deploy

### Detailed Deployment Steps

#### 1. Prepare Your Repository
- Ensure all changes are committed and pushed to GitHub
- Verify `Procfile`, `requirements.txt`, and `runtime.txt` are in the root directory

#### 2. Create Railway Project
1. Go to [Railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Django project

#### 3. Configure Environment Variables
In Railway dashboard, go to your project → Variables tab, add:

```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=0
ALLOWED_HOSTS=your-app-name.railway.app,localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

**Generate a secure SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 4. Set Build and Start Commands
In Railway dashboard → Settings → Deploy:

- **Build Command**: `cd prediction && python manage.py deploy`
- **Start Command**: `gunicorn prediction.wsgi:application --bind 0.0.0.0:$PORT`

#### 5. Deploy
- Click "Deploy" in Railway dashboard
- Wait for build to complete
- Your app will be available at `https://your-app-name.railway.app`

#### 6. Optional: Add Redis Service
For production Celery functionality:
1. In Railway dashboard → "New" → "Database" → "Add Redis"
2. Copy the Redis URL and update `REDIS_URL` environment variable
3. Redeploy your application

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key for security | `django-insecure-...` |
| `DEBUG` | Debug mode (0 for production) | `0` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `your-app.railway.app,localhost` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |

## Production Features

- **Security**: Environment-based configuration, secure secret key handling
- **Performance**: WhiteNoise for static file serving, Gunicorn WSGI server
- **Monitoring**: Comprehensive logging and error handling
- **Scalability**: Celery for background tasks, Redis for caching
- **Reliability**: Automatic migrations and static file collection on deploy

## API Endpoints

- `GET /` - Home page
- `GET /about/` - About page
- `GET /contact/` - Contact page
- `GET /pr/` - Prediction form
- `POST /pr/` - Submit prediction request

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact us through the [Contact page](https://your-app.railway.app/contact/)
- Email: support@smart-housing.com
