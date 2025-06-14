# Imagen base minimalista
FROM python:3.10-slim-bookworm

# Actualiza los paquetes del sistema para reducir vulnerabilidades

# Variables para que Python no genere .pyc y tenga logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la app
COPY app ./app

# Creamos carpeta para la BD (persistirá mientras el contenedor exista)
RUN mkdir /data

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080"]
