# Use la imagen base de Python 3.10
FROM python:3.10-slim

# Establece la variable de entorno PYTHONUNBUFFERED en 1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo en /items_3b/app
WORKDIR /items_3b/app

# Copia el archivo pyproject.toml y el archivo poetry.lock para instalar las dependencias
COPY pyproject.toml poetry.lock /items_3b/app/

# Instala poetry y las dependencias del proyecto
RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copia el resto de los archivos al directorio de trabajo
COPY . .

# Expone el puerto 8000 para que se pueda acceder a la aplicación FastAPI
EXPOSE 8000

# Comando de inicio para ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
