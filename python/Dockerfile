# Stage 1: builder — install dependencies
FROM python:3.12 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Stage 2: final slim image
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application source
COPY app.py .
COPY routes/ routes/
COPY services/ services/
COPY repositories/ repositories/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 5005

CMD ["python", "app.py"]
