# Use Python 3.11 slim image
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput --settings=fteback.settings_prod

# Configurar variables de entorno
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=fteback.settings_prod

# Exponer el puerto
EXPOSE 8080

# Comando para iniciar la aplicación
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 fteback.wsgi:application 