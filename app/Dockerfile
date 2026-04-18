# Imagen base ligera de Python 3.12
# Se usa la variante "slim" para reducir el tamaño del contenedor
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
# Todas las operaciones siguientes se ejecutarán desde /app
WORKDIR /app

# Copia el archivo de dependencias al contenedor
# Se hace primero para aprovechar el cache de Docker en builds futuros
COPY requirements.txt .

# Instala las dependencias necesarias para la aplicación
# --no-cache-dir evita almacenar archivos temporales y reduce el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente al contenedor
# Incluye la aplicación FastAPI, templates, estáticos, etc.
COPY . .

# Comando por defecto al iniciar el contenedor
# Ejecuta el servidor ASGI Uvicorn levantando la app FastAPI
# --host 0.0.0.0 permite acceso desde fuera del contenedor
# --port 8000 define el puerto interno del servicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]