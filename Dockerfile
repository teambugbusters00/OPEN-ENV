FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir fastapi uvicorn

# Expose port
EXPOSE 7860

# Run FastAPI application
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
