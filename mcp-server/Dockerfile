# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only the mcp-server directory contents
COPY . /app/

# Copy stores directory from parent
COPY ../stores /app/stores

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/mcp')"

# Run the server
CMD ["python", "server.py"]

