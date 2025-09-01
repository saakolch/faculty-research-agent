# Deployment Guide - HKUST-GZ Faculty Research Agent

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Free)
1. **Sign up**: Go to [render.com](https://render.com) and create account
2. **Connect GitHub**: Link your GitHub repository
3. **Create Web Service**: 
   - Choose your repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. **Deploy**: Click deploy and wait 2-3 minutes

### Option 2: Railway (Free with $5 credit)
1. **Sign up**: Go to [railway.app](https://railway.app)
2. **Deploy from GitHub**: Connect your repo
3. **Auto-deploy**: Railway will detect Flask app and deploy automatically

### Option 3: Heroku (Paid - $7/month)
1. **Install Heroku CLI**: Download from [heroku.com](https://heroku.com)
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku main`

## 📁 Required Files for Deployment

Your project already includes all necessary files:
- ✅ `Procfile` - Tells deployment platform how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Lists all dependencies
- ✅ `app.py` - Updated for deployment

## 🔧 Deployment-Specific Considerations

### Web Scraping Limitations
Most free hosting platforms have limitations for web scraping:
- **Render**: Limited browser automation
- **Railway**: Better for scraping
- **Heroku**: Good for scraping but paid

### Alternative: Use Sample Data
For free hosting, you can:
1. Pre-scrape data locally
2. Upload JSON files to the deployed app
3. Use the "Load Existing Data" feature

### Environment Variables
Set these in your deployment platform:
```
OPENAI_API_KEY=your_openai_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## 🌐 Step-by-Step Render Deployment

### 1. Prepare Your Repository
```bash
# Make sure all files are committed to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `faculty-research-agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

### 3. Set Environment Variables
In Render dashboard:
- Go to your service → Environment
- Add variables:
  - `OPENAI_API_KEY` (optional)
  - `FLASK_SECRET_KEY` (any random string)

### 4. Deploy
Click "Create Web Service" and wait for deployment.

## 🔄 Continuous Deployment

Once deployed, your app will:
- Auto-deploy when you push to GitHub
- Be accessible 24/7 (with Render's sleep limitations)
- Scale automatically if needed

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | 750 hrs/month | $7/month | Easy deployment |
| **Railway** | $5 credit | Pay per use | Development |
| **Heroku** | None | $7/month | Production |
| **PythonAnywhere** | Limited | $5/month | Python apps |

## 🛠 Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` for compatibility
2. **App crashes**: Check logs in deployment dashboard
3. **Scraping doesn't work**: Use sample data instead
4. **Memory issues**: Optimize for free tier limits

### Logs and Debugging:
- Render: Service → Logs
- Railway: Deployments → View logs
- Heroku: `heroku logs --tail`

## 📊 Performance Optimization

For free hosting:
1. **Reduce dependencies**: Remove unused packages
2. **Use sample data**: Pre-scrape locally
3. **Optimize models**: Use smaller sentence transformers
4. **Cache results**: Store processed data

## 🔐 Security Considerations

1. **API Keys**: Never commit to GitHub
2. **Environment Variables**: Use platform's secure storage
3. **HTTPS**: Most platforms provide automatically
4. **Rate Limiting**: Implement to avoid abuse

## 🎯 Recommended Approach

**For Free Forever:**
1. Use **Render** for the web interface
2. Pre-scrape data locally and upload
3. Use sample data for demonstrations
4. Set up GitHub for continuous deployment

**For Production:**
1. Use **Heroku** or **Railway** paid plans
2. Implement proper error handling
3. Add monitoring and logging
4. Set up automated backups

## 📞 Support

If deployment fails:
1. Check the platform's documentation
2. Review error logs
3. Test locally first
4. Consider using sample data initially

Your app is now ready for deployment! 🚀 