# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy stores directory (data)
COPY stores /app/stores

# Copy mcp-server code
COPY mcp-server /app/mcp-server

# Install Python dependencies
WORKDIR /app/mcp-server
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/mcp')"

# Run the server
CMD ["python", "server.py"]

