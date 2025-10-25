# Railway Deployment Guide for Smart-Housing

This guide provides step-by-step instructions for deploying the Smart-Housing Django application to Railway.

## Prerequisites

- GitHub account with your Smart-Housing repository
- Railway account (free tier available)
- Basic understanding of environment variables

## Step-by-Step Deployment Process

### Step 1: Prepare Your Repository

1. **Ensure all files are committed and pushed to GitHub:**
   ```bash
   git add .
   git commit -m "Production-ready Smart-Housing app"
   git push origin main
   ```

2. **Verify these files exist in your repository root:**
   - `Procfile`
   - `requirements.txt`
   - `runtime.txt`
   - `prediction/` (Django project directory)

### Step 2: Create Railway Account and Project

1. **Go to Railway.app:**
   - Visit [https://railway.app](https://railway.app)
   - Sign up using your GitHub account

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your Smart-Housing repository
   - Railway will automatically detect it's a Django project

### Step 3: Configure Environment Variables

1. **Navigate to your project dashboard**
2. **Go to Variables tab**
3. **Add the following environment variables:**

   ```
   DJANGO_SECRET_KEY=django-insecure-unique-secret-key-here
   DEBUG=0
   ALLOWED_HOSTS=app-name.railway.app,localhost,127.0.0.1
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Generate a secure SECRET_KEY:**
   ```python
   # Run this in Python to generate a secure key
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

### Step 4: Configure Build and Start Commands

1. **Go to Settings → Deploy**
2. **Set Build Command:**
   ```
   cd prediction && python manage.py deploy
   ```

3. **Set Start Command:**
   ```
   gunicorn prediction.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Step 5: Deploy Your Application

1. **Click "Deploy" in the Railway dashboard**
2. **Wait for the build process to complete** (usually 2-5 minutes)
3. **Monitor the deployment logs** for any errors
4. **Your app will be available at:** `https://app-name.railway.app`

### Step 6: Verify Deployment

1. **Visit your deployed URL**
2. **Test the following pages:**
   - Home page: `https://app-name.railway.app/`
   - About page: `https://app-name.railway.app/about/`
   - Contact page: `https://app-name.railway.app/contact/`
   - Prediction form: `https://smart-housing.up.railway.app/predict/`

3. **Test the prediction functionality:**
   - Fill out the form with sample data
   - Submit and verify you get a price prediction

### Step 7: Optional - Add Redis Service (for Celery)

If you want to enable background task processing:

1. **In Railway dashboard → "New" → "Database" → "Add Redis"**
2. **Copy the Redis connection URL**
3. **Update the `REDIS_URL` environment variable**
4. **Redeploy your application**

## Troubleshooting Common Issues

### Build Failures

**Issue:** Build command fails
**Solution:** 
- Check that `cd prediction && python manage.py deploy` is correct
- Ensure all dependencies are in `requirements.txt`
- Check deployment logs for specific error messages

### Static Files Not Loading

**Issue:** CSS/images not displaying
**Solution:**
- Verify `STATIC_ROOT` is set in settings.py
- Ensure `collectstatic` runs during build
- Check that WhiteNoise is properly configured

### Environment Variables Not Working

**Issue:** App crashes with configuration errors
**Solution:**
- Double-check environment variable names and values
- Ensure no extra spaces in variable values
- Verify `DEBUG=0` (not `False` or `false`)

### Database Issues

**Issue:** Database connection errors
**Solution:**
- SQLite is used by default (no additional setup needed)
- For PostgreSQL, add Railway's PostgreSQL service
- Update `DATABASES` setting in `settings.py`

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Yes | Django secret key for security | `django-insecure-...` |
| `DEBUG` | Yes | Debug mode (0 for production) | `0` |
| `ALLOWED_HOSTS` | Yes | Comma-separated allowed hosts | `app.railway.app,localhost` |
| `REDIS_URL` | No | Redis connection URL (for Celery) | `redis://localhost:6379/0` |

## Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] All pages are accessible
- [ ] Prediction form works correctly
- [ ] Static files (CSS, images) load properly
- [ ] Contact form shows success message
- [ ] Mobile responsiveness works
- [ ] Environment variables are properly set
- [ ] Build and start commands are configured

## Monitoring and Maintenance

1. **Monitor your application:**
   - Check Railway dashboard for resource usage
   - Monitor deployment logs for errors
   - Set up alerts for downtime

2. **Regular updates:**
   - Keep dependencies updated
   - Monitor security advisories
   - Backup your data regularly

3. **Scaling considerations:**
   - Railway automatically handles basic scaling
   - Consider upgrading to paid plan for production use
   - Monitor performance metrics

## Support and Resources

- **Railway Documentation:** [https://docs.railway.app](https://docs.railway.app)
- **Django Deployment Guide:** [https://docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)
- **Project Issues:** Create an issue on GitHub
- **Contact:** Use the contact form on your deployed application

## Cost Considerations

- **Railway Free Tier:** 500 hours/month, $5 credit
- **Paid Plans:** Start at $5/month for production use
- **Additional Services:** Redis, PostgreSQL, etc. have separate costs

Your Smart-Housing application is now ready for production use! 🚀
