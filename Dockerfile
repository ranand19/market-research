# Market Research App - Multi-stage Docker build
FROM node:18-alpine as frontend-build

# Build the React frontend
WORKDIR /app/frontend
COPY MarketResearchUI/package*.json ./
RUN npm install
COPY MarketResearchUI/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application
COPY api_backend.py .
COPY agents/ ./agents/
COPY tools/ ./tools/
COPY .env .env.example

# Copy the built frontend from the previous stage
COPY --from=frontend-build /app/frontend/build ./static

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["uvicorn", "api_backend:app", "--host", "0.0.0.0", "--port", "8080"]