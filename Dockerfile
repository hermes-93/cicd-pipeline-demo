# =============================================================================
# Stage 1 — builder
# Install dependencies into a virtual environment so only the venv gets copied
# to the final image, keeping it lean and free of build tools.
# =============================================================================
FROM python:3.14-slim AS builder

WORKDIR /build

# Install deps before copying app code so this layer is cached on code changes
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# =============================================================================
# Stage 2 — runtime
# Minimal image: no pip, no build tools, just the app and its venv.
# =============================================================================
FROM python:3.14-slim AS runtime

# Run as non-root for security
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy the pre-built venv from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source
COPY app/ ./app/

# Make venv the default Python environment
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 8000

# Use exec form so uvicorn receives SIGTERM directly (graceful shutdown)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
