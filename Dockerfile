# Usamos una versión oficial estable de Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema esenciales para PyNaCl y FFmpeg
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalar requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del bot
COPY . .

CMD ["python", "bot.py"]