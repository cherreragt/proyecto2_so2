# Sistema de Registro de Puntos de Interés con Base de Datos Geoespacial

## Descripción
Aplicación web contenerizada para registrar y consultar puntos de interés con ubicación geográfica.

## Tecnologías usadas
- PostgreSQL + PostGIS
- FastAPI
- Nginx
- Docker Compose

## Arquitectura
- db: base de datos geoespacial
- app: API REST
- proxy: punto de entrada único

## Requisitos
- Docker
- Docker Compose

## Configuración
Crear archivo `.env` con:
...

## Ejecución
docker compose up --build

## Acceso
- Aplicación: http://localhost
- Documentación API: http://localhost/docs

## Endpoints principales
- GET /points
- GET /points?category=...
- GET /points/nearby?lat=...&lon=...&radius=...
- POST /points

## Persistencia
Se usa un volumen Docker para los datos PostgreSQL.

## Datos iniciales
Se insertan 5 puntos de ejemplo automáticamente al iniciar.