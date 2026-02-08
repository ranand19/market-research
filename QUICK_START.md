# 🚀 Quick Start Guide
## Market Research & Competitor Tracking Platform

Get up and running in **less than 10 minutes**!

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- ✅ Python 3.9 or higher installed
- ✅ Node.js 16.x or higher installed
- ✅ OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))
- ✅ Terminal/Command prompt access
- ✅ Text editor or IDE

---

## 🎯 Step-by-Step Setup

### Step 1: Navigate to Project Directory

```bash
cd /Users/ranan06/Projects/Agentic/market-research-app
```

### Step 2: Set Up Python Backend

#### 2.1 Create Virtual Environment
```bash
python3 -m venv venv
```

#### 2.2 Activate Virtual Environment
**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- LangChain (AI agent framework)
- OpenAI (LLM integration)
- And other required packages

#### 2.4 Configure OpenAI API Key

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

**Replace** `your_openai_api_key_here` with your actual OpenAI API key.

#### 2.5 Start the Backend Server
```bash
python api_backend.py
```

✅ **Success!** You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The backend must run continuously.

---

### Step 3: Set Up React Frontend

#### 3.1 Open a New Terminal
Keep the backend running and open a **new terminal window**.

#### 3.2 Navigate to Frontend Directory
```bash
cd /Users/ranan06/Projects/Agentic/market-research-app/MarketResearchUI
```

#### 3.3 Install Node Dependencies
```bash
npm install
```

This may take a few minutes. Coffee break? ☕

#### 3.4 Start the Frontend Server
```bash
npm start
```

✅ **Success!** Your browser should automatically open to `http://localhost:3000`

If not, manually navigate to: **http://localhost:3000**

---

## 🎉 You're Ready!

You should now see the **Market Research & Competitor Tracking** interface with:
- Albertsons branding in the header
- Research query input form
- Research type selector
- "AI Backend Active" status indicator (green dot)

---

## 🧪 Quick Test

### Test 1: Health Check
Verify the backend is working:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Market Research & Competitor Tracking API",
  "version": "1.0.0",
  "llm_available": true
}
```

### Test 2: Run a Research Query

**In the UI:**
1. Enter a query: `"Analyze organic food market trends"`
2. Select research type: `Market Overview`
3. Optional: Enter industry: `Retail Grocery`
4. Click **"Start Research"**

**Expected result:**
- Loading indicator appears
- Results screen displays with comprehensive analysis
- Executive summary and detailed findings

---

## 📊 Usage Guide

### Research Types

1. **Market Overview** 🎯
   - Market size and growth analysis
   - Key trends and opportunities
   - Industry segmentation
   - **Best for**: Understanding overall market landscape

2. **Competitor Analysis** 👥
   - Competitor profiling
   - SWOT analysis
   - Market positioning
   - **Best for**: Understanding competitive dynamics

3. **Trend Analysis** 📈
   - Emerging trends identification
   - Future predictions
   - Technology and consumer trends
   - **Best for**: Forward-looking strategic planning

4. **Full Report** 📋
   - Combines all analysis types
   - Comprehensive research
   - Executive summary
   - **Best for**: Complete market intelligence

---

## 🔧 Common Issues & Solutions

### ❌ Backend won't start

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### ❌ OpenAI API Error

**Issue**: `openai.error.AuthenticationError`

**Solution**:
- Check your `.env` file exists in the project root
- Verify your API key is correct (no extra spaces)
- Ensure you have credits in your OpenAI account
- Test your key at: https://platform.openai.com/account/api-keys

---

### ❌ Frontend shows "Backend Offline"

**Issue**: Orange indicator instead of green

**Solution**:
1. Check backend is running (terminal should show "Uvicorn running")
2. Test backend: `curl http://localhost:8000/health`
3. Check no other service is using port 8000:
   ```bash
   lsof -i :8000  # macOS/Linux
   ```
4. Restart backend if needed

---

### ❌ npm install fails

**Issue**: Errors during `npm install`

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

### ❌ Port 3000 already in use

**Issue**: `Port 3000 is already in use`

**Solution**:
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9  # macOS/Linux

# Or start on a different port
PORT=3001 npm start
```

---

## 🎯 Example Queries

Try these research queries to explore the platform:

### Market Research
```
Query: "Analyze the plant-based meat alternatives market"
Type: Market Overview
Industry: Food & Beverage
```

### Competitor Analysis
```
Query: "Compare grocery delivery services"
Type: Competitor Analysis
Company: Albertsons
Competitors: Instacart, Amazon Fresh, Walmart+
```

### Trend Analysis
```
Query: "What are the key trends in sustainable retail?"
Type: Trend Analysis
Industry: Retail
```

### Full Report
```
Query: "Comprehensive analysis of the organic grocery market"
Type: Full Report
Industry: Organic Retail
Competitors: Whole Foods, Sprouts, Trader Joe's
```

---

## 📚 Next Steps

1. **Explore Features**: Try different research types
2. **Download Reports**: Use the download button on results screen
3. **Review API Docs**: Visit http://localhost:8000/docs
4. **Customize**: Modify queries for your specific needs
5. **Read Full Docs**: Check out [README.md](./README.md) for advanced features

---

## 🛑 Stopping the Application

### Stop Frontend
In the frontend terminal: `Ctrl + C`

### Stop Backend
In the backend terminal: `Ctrl + C`

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 📞 Need Help?

If you encounter issues not covered here:

1. Check the main [README.md](./README.md)
2. Review backend logs in the terminal
3. Check browser console for frontend errors (F12 → Console)
4. Verify all prerequisites are installed correctly

---

## ✅ Success Checklist

Before considering setup complete:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Green "AI Backend Active" indicator visible
- [ ] Successfully executed a test research query
- [ ] Results displayed correctly
- [ ] No console errors

---

**🎉 Congratulations! You're ready to conduct AI-powered market research!**

---

*Built for Albertsons Companies | Powered by LangChain & OpenAI*
