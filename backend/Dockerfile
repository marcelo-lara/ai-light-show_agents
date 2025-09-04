# Frontend build stage
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# Copy package.json and package-lock.json first for better cache utilization
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source files
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Backend build stage
FROM python:3.10-slim

WORKDIR /app

# Copy backend requirements first for better cache utilization
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt && \
    pip install gunicorn eventlet

# Copy backend files
COPY backend/ ./backend/

# Copy other necessary directories
COPY common/ ./common/
COPY data/ ./data/
COPY songs/ ./songs/
COPY fixtures/ ./fixtures/ 

# Copy the built frontend from the frontend-build stage
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "backend.app:app"]
