# Imagen base ligera
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos la librería necesaria para MySQL
RUN pip install mysql-connector-python

# Copiamos el script al contenedor
COPY backup_script.py .

# Creamos la carpeta para el volumen de datos
RUN mkdir /data

# Ejecutamos el script
CMD ["python", "backup_script.py"]