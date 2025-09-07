# 🚨 Fix Render Deployment - Internal Server Error

## The Problem
Your Render app at `https://sml-com.onrender.com` is showing "Internal Server Error" because of configuration issues.

## ✅ Quick Fix

### 1. **Update Your Render Service**
Go to your Render dashboard and update these settings:

**Environment Variables:**
- `DJANGO_SETTINGS_MODULE` = `spoorthi_macs.settings` (not settings_production)
- `DEBUG` = `False`
- `SECRET_KEY` = Generate a new secure key
- `DATABASE_URL` = Should be auto-set by Render

### 2. **Generate a New SECRET_KEY**
Run this command locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. **Update Render Build Command**
In your Render service settings, set the build command to:
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

### 4. **Update Start Command**
Set the start command to:
```bash
gunicorn spoorthi_macs.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

## 🔧 Alternative: Manual Deploy

If the above doesn't work, try this:

1. **Delete your current Render service**
2. **Create a new one** using the updated `render.yaml`
3. **Connect your GitHub repo**
4. **Deploy fresh**

## 🎯 Expected Result

After the fix, your app should be accessible at:
- `https://sml-com.onrender.com` (or your new service name)
- Admin: `https://sml-com.onrender.com/admin/`
- Login: `admin` / `admin123`

## 🆘 If Still Not Working

Check the Render build logs for specific error messages. The most common issues are:

1. **Missing dependencies** - Check requirements.txt
2. **Database connection** - Verify DATABASE_URL
3. **Settings module** - Ensure DJANGO_SETTINGS_MODULE is correct
4. **Static files** - Check collectstatic command

## 📞 Quick Test

Run this locally to verify everything works:
```bash
python debug_render.py
```

This will check all components and tell you what's wrong.
