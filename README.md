# Market Research & Competitor Tracking Platform

## 🎯 Overview

An AI-powered market research and competitor tracking application built for business users at Albertsons Companies. This platform leverages **LangChain agents** to provide intelligent market analysis, competitor insights, trend predictions, and comprehensive research reports.

## ✨ Features

### 🔍 Research Capabilities
- **Market Overview Analysis**: Comprehensive market size, trends, and opportunities
- **Competitor Analysis**: Deep dive into competitor strategies, strengths, and weaknesses
- **Trend Analysis**: Identify emerging trends and future market predictions
- **Full Research Reports**: Multi-dimensional analysis combining all research types

### 🤖 AI-Powered Tools
- **Market Research Agent**: Analyzes market dynamics and opportunities
- **Competitor Analysis Agent**: Profiles competitors and their strategies
- **Trend Analysis Agent**: Identifies patterns and future predictions
- **Customer Insights Agent**: Understands customer preferences and behaviors
- **Pricing Analysis Agent**: Evaluates pricing strategies and positioning

### 🎨 User Interface
- Modern React-based UI with Material-UI components
- Albertsons brand colors and styling
- Intuitive research query builder
- Interactive results visualization
- Downloadable research reports

## 🏗️ Architecture

### Backend (Python)
- **Framework**: FastAPI
- **AI Framework**: LangChain with OpenAI GPT-4
- **Agents**: Multiple specialized research agents
- **API**: RESTful endpoints for research execution

### Frontend (React)
- **Framework**: React 18
- **UI Library**: Material-UI (MUI)
- **State Management**: React Hooks
- **API Client**: Axios

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher
- **OpenAI API Key**: Required for LLM functionality

## 🚀 Quick Start

See [QUICK_START.md](./QUICK_START.md) for detailed setup instructions.

### Backend Setup

1. **Navigate to project directory**:
   ```bash
   cd market-research-app
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. **Start the backend server**:
   ```bash
   python api_backend.py
   ```
   
   Backend will run at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd MarketResearchUI
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```
   
   Frontend will run at: `http://localhost:3000`

## 📚 API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `GET /health` - Health check
- `GET /research/types` - Get available research types
- `GET /tools/list` - List available AI tools
- `POST /research/execute` - Execute research query

### Example API Request

```bash
curl -X POST http://localhost:8000/research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze the organic food market trends",
    "research_type": "market_overview",
    "industry": "Retail Grocery",
    "company_name": "Albertsons",
    "competitors": ["Kroger", "Walmart", "Whole Foods"]
  }'
```

## 🎨 Branding

The application features Albertsons Companies branding:
- **Primary Color**: Albertsons Blue (#003da5)
- **Secondary Color**: Albertsons Orange (#ff6b35)
- **Typography**: Modern, professional font stack
- **Logo**: Albertsons Companies branding in header

## 🔧 Configuration

### Backend Configuration
Edit `api_backend.py` to customize:
- Port number (default: 8000)
- LLM model (default: gpt-4)
- API timeout settings
- CORS settings

### Frontend Configuration
Create `.env` file in `MarketResearchUI/`:
```
REACT_APP_API_URL=http://localhost:8000
```

## 📊 Usage Examples

### 1. Market Overview Research
```
Query: "Analyze the plant-based food market in North America"
Research Type: Market Overview
Industry: Food & Beverage
```

### 2. Competitor Analysis
```
Query: "Compare Albertsons vs. competitors in digital grocery"
Research Type: Competitor Analysis
Company: Albertsons
Competitors: Kroger, Walmart, Amazon Fresh
```

### 3. Trend Analysis
```
Query: "What are the emerging trends in retail grocery?"
Research Type: Trend Analysis
Industry: Retail Grocery
```

## 🛠️ Development

### Project Structure
```
market-research-app/
├── api_backend.py           # FastAPI backend with LangChain agents
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
└── MarketResearchUI/       # React frontend
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── index.js
        ├── components/
        │   ├── ResearchInputScreen.js
        │   └── ResearchResultsScreen.js
        ├── services/
        │   └── apiService.js
        └── styles/
            └── theme.js
```

### Adding New Research Tools
1. Define tool function in `api_backend.py`
2. Add tool to `tools` list
3. Update frontend research types if needed

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Research Execution
```bash
curl -X POST http://localhost:8000/research/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "Test query", "research_type": "market_overview"}'
```

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Verify all dependencies installed: `pip list`
- Check OPENAI_API_KEY is set in .env file
- Ensure port 8000 is not in use

### Frontend won't start
- Check Node.js version: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check backend is running
- Verify API_URL in frontend .env

### API returns errors
- Check OpenAI API key is valid
- Verify backend logs for detailed error messages
- Check network connectivity
- Review request payload format

## 📦 Deployment

### Backend Deployment
- Use production WSGI server (e.g., Gunicorn)
- Configure environment variables
- Set up HTTPS/SSL
- Implement authentication/authorization
- Add rate limiting

### Frontend Deployment
```bash
cd MarketResearchUI
npm run build
# Deploy build/ directory to hosting service
```

## 🔒 Security Notes

- Store API keys securely (use environment variables)
- Implement authentication for production use
- Add rate limiting to prevent abuse
- Validate all user inputs
- Use HTTPS in production

## 📝 License

© 2026 Albertsons Companies, Inc. All rights reserved.

## 🤝 Support

For questions or issues:
- Review the [QUICK_START.md](./QUICK_START.md) guide
- Check API documentation at `/docs`
- Review backend logs for errors

## 🎯 Roadmap

- [ ] Add user authentication
- [ ] Implement research history/saved reports
- [ ] Add real-time data source integrations
- [ ] Create PDF export functionality
- [ ] Add collaborative features
- [ ] Implement advanced visualization charts
- [ ] Add email report delivery

---

**Built with ❤️ for Albertsons Companies**
