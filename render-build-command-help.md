# 🔧 Render.com Build Command Help

## 🎯 **Where to Find Build Command in Render.com:**

### **Step 1: After Connecting Repository**
1. **Repository connected:** ✅ `infinite-quantum-god-rahul/rahul-l`
2. **Branch selected:** ✅ `main`

### **Step 2: Scroll Down to Advanced Settings**
1. **Look for "Advanced" section** (usually at the bottom)
2. **Click "Advanced" to expand**
3. **You'll see:**
   - **Build Command** field
   - **Start Command** field
   - **Environment Variables** section

### **Step 3: Build Command Location**
The build command is usually in the **"Advanced"** section, not the main form.

---

## 🔧 **Exact Build Command to Enter:**

```
pip install -r requirements.txt
```

---

## 🚀 **Complete Render.com Configuration:**

### **Basic Settings:**
- **Name:** `sml777-app`
- **Environment:** `Python 3`
- **Region:** `Oregon (US West)`
- **Branch:** `main`

### **Advanced Settings (Click "Advanced"):**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn spoorthi_macs.wsgi:application --bind 0.0.0.0:$PORT`

### **Environment Variables:**
- `DJANGO_SETTINGS_MODULE` = `spoorthi_macs.settings`
- `DEBUG` = `False`
- `SECRET_KEY` = `your-secret-key-here`
- `ALLOWED_HOSTS` = `*.onrender.com`

---

## 🔍 **If You Still Don't See Build Command:**

### **Option 1: Look for "Advanced" Button**
1. **Scroll to bottom** of the form
2. **Look for "Advanced" or "Show Advanced" button**
3. **Click it** to expand more options

### **Option 2: Check Different Sections**
1. **"Build & Deploy"** section
2. **"Environment"** section
3. **"Settings"** section

### **Option 3: Try Different Render.com Interface**
1. **Refresh the page**
2. **Try creating a new web service**
3. **Make sure you're on the correct page**

---

## 📱 **Screenshot Guide:**

```
Render.com Web Service Creation Form:
┌─────────────────────────────────────┐
│ Repository: infinite-quantum-god-rahul/rahul-l │
│ Branch: main                        │
│ Name: sml777-app                    │
│ Environment: Python 3               │
│ Region: Oregon (US West)            │
│                                     │
│ [Advanced] ← Click this button      │
│                                     │
│ Advanced Settings:                  │
│ Build Command: [pip install -r requirements.txt] │
│ Start Command: [gunicorn spoorthi_macs.wsgi:application --bind 0.0.0.0:$PORT] │
│                                     │
│ Environment Variables:              │
│ DJANGO_SETTINGS_MODULE = spoorthi_macs.settings │
│ DEBUG = False                       │
│ SECRET_KEY = your-secret-key-here   │
│ ALLOWED_HOSTS = *.onrender.com      │
│                                     │
│ [Create Web Service]                │
└─────────────────────────────────────┘
```

---

## 🆘 **Still Can't Find It?**

### **Alternative: Use render.yaml**
If you can't find the build command field, Render.com will automatically use the `render.yaml` file I created, which contains:

```yaml
services:
  - type: web
    name: sml777-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn spoorthi_macs.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: spoorthi_macs.settings
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: *.onrender.com
```

---

## 🎯 **Quick Fix:**

1. **Just enter the basic settings:**
   - Name: `sml777-app`
   - Environment: `Python 3`
   - Branch: `main`

2. **Click "Create Web Service"**
3. **Render will use the `render.yaml` file automatically**
4. **Your app will deploy successfully!**

---

## 🚀 **Success!**

Once deployed, your app will be available at:
```
https://sml777-app.onrender.com
```

**The build command is there - just look for the "Advanced" section!** 🔍


