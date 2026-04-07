CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS points_of_interest (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_poi_location
ON points_of_interest
USING GIST (location);

INSERT INTO points_of_interest (name, description, category, latitude, longitude, location)
VALUES
(
    'Palacio Nacional',
    'Edificio histórico en el centro de la ciudad',
    'cultural',
    14.6417,
    -90.5133,
    ST_SetSRID(ST_MakePoint(-90.5133, 14.6417), 4326)::geography
),
(
    'Zoológico La Aurora',
    'Parque zoológico de la ciudad',
    'natural',
    14.5837,
    -90.5270,
    ST_SetSRID(ST_MakePoint(-90.5270, 14.5837), 4326)::geography
),
(
    'Museo Popol Vuh',
    'Museo arqueológico y cultural',
    'cultural',
    14.6045,
    -90.4896,
    ST_SetSRID(ST_MakePoint(-90.4896, 14.6045), 4326)::geography
),
(
    'Gasolinera Centro',
    'Estación de servicio urbana',
    'gastronomico',
    14.6349,
    -90.5069,
    ST_SetSRID(ST_MakePoint(-90.5069, 14.6349), 4326)::geography
),
(
    'Parque Ecológico',
    'Área verde y recreativa',
    'natural',
    14.6200,
    -90.5400,
    ST_SetSRID(ST_MakePoint(-90.5400, 14.6200), 4326)::geography
);