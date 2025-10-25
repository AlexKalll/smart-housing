# 🔧 CSRF Fix for Railway Production

## Issue
CSRF verification failed (403 error) when submitting forms in production at `https://smart-housing.up.railway.app/predict/`

## ✅ Solution Applied

### 1. Updated Django Settings
Added CSRF configuration to `prediction/prediction/settings.py`:

```python
# CSRF Configuration for Production
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://smart-housing.up.railway.app,https://*.up.railway.app', cast=lambda v: [s.strip() for s in v.split(',')])
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Session Configuration for Production
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

### 2. Add Environment Variable in Railway
Add this environment variable in your Railway dashboard:

**Variable Name:** `CSRF_TRUSTED_ORIGINS`
**Variable Value:** `https://smart-housing.up.railway.app,https://*.up.railway.app`

### 3. Redeploy
After adding the environment variable, redeploy your application.

## 🔍 What This Fixes

- **CSRF Trusted Origins**: Tells Django which domains are trusted for CSRF tokens
- **Secure Cookies**: Ensures CSRF and session cookies work properly with HTTPS
- **SameSite Policy**: Prevents CSRF attacks while allowing legitimate requests

## ✅ After Fix

Your prediction form at `https://smart-housing.up.railway.app/predict/` will work without CSRF errors!

## 📋 Complete Environment Variables

Make sure you have ALL these variables set in Railway:

```
DJANGO_SECRET_KEY=a-#gqkp7ug+hs7ma05-n!ser_p*m@)lq4c!rtn&)q_9%0xwu4-
DEBUG=0
ALLOWED_HOSTS=smart-housing.up.railway.app,healthcheck.railway.app,*.up.railway.app,localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
CSRF_TRUSTED_ORIGINS=https://smart-housing.up.railway.app,https://*.up.railway.app
```

Your Smart-Housing app will now work perfectly in production! 🚀
