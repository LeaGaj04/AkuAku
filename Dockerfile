FROM python:3.11-slim

# Instalar ffmpeg y dependencias nativas del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libsodium-dev \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Puerto para el health check de Koyeb
EXPOSE 8000

# Ejecutar el bot
CMD ["python", "bot.py"]
