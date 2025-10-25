# Railway Environment Variables Configuration
# For: https://smart-housing.railway.app

## 🔐 Environment Variables to Set in Railway Dashboard

### Required Variables:

```
DJANGO_SECRET_KEY=a-#gqkp7ug+hs7ma05-n!ser_p*m@)lq4c!rtn&)q_9%0xwu4-
DEBUG=0
ALLOWED_HOSTS=smart-housing.railway.app,healthcheck.railway.app,*.up.railway.app,localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

### Optional Variables (for enhanced functionality):

```
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

## 📋 Step-by-Step Railway Configuration

### 1. Access Railway Dashboard
- Go to [railway.app](https://railway.app)
- Sign in with your GitHub account
- Navigate to your project

### 2. Set Environment Variables
1. Click on your project
2. Go to **"Variables"** tab
3. Click **"New Variable"** for each variable below:

#### Variable 1: DJANGO_SECRET_KEY
- **Name**: `DJANGO_SECRET_KEY`
- **Value**: `a-#gqkp7ug+hs7ma05-n!ser_p*m@)lq4c!rtn&)q_9%0xwu4-`

#### Variable 2: DEBUG
- **Name**: `DEBUG`
- **Value**: `0`

#### Variable 3: ALLOWED_HOSTS
- **Name**: `ALLOWED_HOSTS`
- **Value**: `smart-housing.up.railway.app,healthcheck.railway.app,*.up.railway.app,localhost,127.0.0.1`

#### Variable 4: REDIS_URL
- **Name**: `REDIS_URL`
- **Value**: `redis://localhost:6379/0`

### 3. Configure Build Commands
1. Go to **"Settings"** tab
2. Click **"Deploy"**
3. Set the following commands:

#### Build Command:
```
cd prediction && python manage.py deploy
```

#### Start Command:
```
cd prediction && gunicorn prediction.wsgi:application --bind 0.0.0.0:$PORT
```

**Note:** The `railway.json` file has been created to automatically configure these commands, so you may not need to set them manually.

### 4. Deploy Your Application
1. Click **"Deploy"** button
2. Wait for build to complete (2-5 minutes)
3. Your app will be live at: **https://smart-housing.up.railway.app**

## 🔧 What Each Variable Does

| Variable | Purpose | Value |
|----------|---------|-------|
| `DJANGO_SECRET_KEY` | Django security key for sessions, CSRF, etc. | Generated secure key |
| `DEBUG` | Debug mode (0 = production, 1 = development) | `0` |
| `ALLOWED_HOSTS` | Domains that can serve your Django app | `smart-housing.railway.app,localhost,127.0.0.1` |
| `REDIS_URL` | Redis connection for Celery tasks | `redis://localhost:6379/0` |

## 🚀 Post-Deployment Verification

After deployment, test these URLs:
- **Home**: https://smart-housing.railway.app/
- **About**: https://smart-housing.railway.app/about/
- **Contact**: https://smart-housing.railway.app/contact/
- **Predict**: https://smart-housing.up.railway.app/predict/

## 🔍 Troubleshooting

### If deployment fails:
1. Check Railway logs for error messages
2. Verify all environment variables are set correctly
3. Ensure build command includes `cd prediction &&`

### If app doesn't load:
1. Verify `ALLOWED_HOSTS` includes `smart-housing.railway.app`
2. Check that `DEBUG=0` (not `False` or `false`)
3. Ensure `DJANGO_SECRET_KEY` is properly set

### If ML predictions don't work:
1. Check that models were created during build
2. Verify `checkpoints/` directory exists
3. Check deployment logs for model creation messages

## 📊 Production Features Enabled

With these settings, your app will have:
- ✅ **Secure Production Mode**: DEBUG=0, secure secret key
- ✅ **Custom Domain**: smart-housing.railway.app
- ✅ **ML Predictions**: Pre-trained models ready
- ✅ **Auto-Retraining**: Celery background tasks
- ✅ **Static Files**: Optimized CSS, JS, images
- ✅ **Mobile Responsive**: Works on all devices

Your Smart-Housing app is now ready for production deployment! 🎉
