FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# ✅ FIX M13: Proper permissions (750, not 777)
RUN mkdir -p /app/uploads && \
    chown appuser:appuser /app/uploads && \
    chmod 750 /app/uploads

# Switch to non-root user
USER appuser

# ✅ FIX M2 & M10: Production settings
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--no-server-header"]