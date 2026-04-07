from fastapi import FastAPI, Depends, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import SessionLocal
from models import PointOfInterest

app = FastAPI(title="POI API", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class PointCreate(BaseModel):
    name: str
    description: str
    category: str
    latitude: float
    longitude: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/api")
def api_root():
    return {"message": "API de puntos de interés funcionando correctamente"}


@app.get("/api/points")
def list_points(
    category: str | None = None,
    db: Session = Depends(get_db)
):
    if category:
        points = db.query(PointOfInterest).filter(PointOfInterest.category == category).all()
    else:
        points = db.query(PointOfInterest).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "latitude": p.latitude,
            "longitude": p.longitude,
        }
        for p in points
    ]


@app.post("/api/points")
def create_point(point: PointCreate, db: Session = Depends(get_db)):
    insert_sql = text("""
        INSERT INTO points_of_interest (name, description, category, latitude, longitude, location)
        VALUES (
            :name,
            :description,
            :category,
            :latitude,
            :longitude,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography
        )
        RETURNING id;
    """)

    result = db.execute(insert_sql, {
        "name": point.name,
        "description": point.description,
        "category": point.category,
        "latitude": point.latitude,
        "longitude": point.longitude
    })
    new_id = result.fetchone()[0]
    db.commit()

    return {"message": "Punto creado correctamente", "id": new_id}


@app.get("/api/points/nearby")
def nearby_points_api(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(..., description="Radio en metros"),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            id,
            name,
            description,
            category,
            latitude,
            longitude,
            ST_Distance(
                location,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
            ) AS distance
        FROM points_of_interest
        WHERE ST_DWithin(
            location,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography,
            :radius
        )
        ORDER BY distance ASC;
    """)

    result = db.execute(query, {"lat": lat, "lon": lon, "radius": radius})
    rows = result.fetchall()

    return [
        {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "category": row.category,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "distance_meters": round(row.distance, 2)
        }
        for row in rows
    ]