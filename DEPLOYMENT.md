# 🚀 SML777 Django Deployment to Render.com

This guide will help you deploy your SML777 Django project to Render.com.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Environment Variables**: Prepare your environment variables

## 🛠️ Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit all files** to your GitHub repository:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Create Render Account & Connect Repository

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your repository
4. Choose the branch (usually `main` or `master`)

### Step 3: Configure Web Service

**Basic Settings:**
- **Name**: `sml777-web` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (project is in root)
- **Runtime**: `Python 3.11.7`

**Build & Deploy:**
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn spoorthi_macs.wsgi:application`

### Step 4: Add PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `sml777-db`
3. **Database**: `sml777`
4. **User**: `sml777_user`
5. **Plan**: Free (for testing) or Starter (for production)
6. **Region**: Same as your web service

### Step 5: Configure Environment Variables

In your web service settings, add these environment variables:

#### Required Variables:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=sml777.onrender.com
```

#### Optional Variables (for features):
```
# Credit Bureau
SML_BUREAU_PROVIDER=CIBIL
CIBIL_BASE_URL=your-cibil-url
CIBIL_API_KEY=your-cibil-key

# Payments
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret

# SMS
ALERT_SMS_URL=your-sms-url
ALERT_SMS_KEY=your-sms-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application

### Step 7: Access Your Application

1. Once deployed, you'll get a URL like: `https://sml777.onrender.com`
2. Your admin account will be created automatically:
   - **Username**: `admin`
   - **Password**: `admin123`
   - **Login URL**: `https://sml777.onrender.com/admin/`

## 🔧 Configuration Files

The following files have been created for deployment:

- `build.sh` - Build script for Render
- `runtime.txt` - Python version specification
- `render.yaml` - Automated deployment configuration
- `env.example` - Environment variables template
- `requirements.txt` - Python dependencies

## 🚨 Important Notes

### Security
- **Change the default admin password** immediately after deployment
- **Use a strong SECRET_KEY** in production
- **Set DEBUG=False** in production
- **Configure proper ALLOWED_HOSTS**

### Database
- **Free PostgreSQL** has limitations (1GB storage, 1 month retention)
- **Upgrade to paid plan** for production use
- **Backup your data** regularly

### Static Files
- Static files are served by WhiteNoise
- Media files are stored in Render's ephemeral filesystem
- **Use cloud storage** (AWS S3, Cloudinary) for production media files

### Performance
- **Free tier** has cold starts (30-second delay after inactivity)
- **Upgrade to paid plan** for better performance
- **Use Redis** for caching in production

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` for missing dependencies
   - Verify Python version in `runtime.txt`
   - Check build logs in Render dashboard

2. **Database Connection Error**:
   - Verify `DATABASE_URL` is set correctly
   - Check database service is running
   - Ensure database credentials are correct

3. **Static Files Not Loading**:
   - Verify `STATIC_ROOT` and `STATIC_URL` settings
   - Check WhiteNoise configuration
   - Run `collectstatic` command

4. **Application Crashes**:
   - Check application logs in Render dashboard
   - Verify all environment variables are set
   - Check for missing dependencies

### Getting Help:
- Check Render documentation: [render.com/docs](https://render.com/docs)
- View application logs in Render dashboard
- Check Django logs for specific errors

## 🎉 Success!

Once deployed, your SML777 application will be available at your Render URL. You can:

1. **Access the admin panel** at `/admin/`
2. **View your application** at the root URL
3. **Monitor performance** in Render dashboard
4. **Scale up** as needed

## 📈 Next Steps

1. **Set up monitoring** (Sentry, New Relic)
2. **Configure backups** for your database
3. **Set up CI/CD** for automatic deployments
4. **Add custom domain** if needed
5. **Implement caching** for better performance

---

**Happy Deploying! 🚀**


