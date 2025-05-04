from sqlalchemy.orm import Session
from shapely.geometry import shape, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from geoalchemy2.shape import from_shape, to_shape
from fastapi import HTTPException
from . import models, schemas
from geojson_pydantic import Point as GeoPoint, LineString as GeoLineString, Polygon as GeoPolygon, MultiPoint as GeoMultiPoint, MultiLineString as GeoMultiLineString, MultiPolygon as GeoMultiPolygon

def wkb_to_geojson(wkb_element):
    """Convert WKB geometry to GeoJSON format."""
    shapely_geometry = to_shape(wkb_element)
    
    if isinstance(shapely_geometry, Point):
        # For Point, we need to convert the coordinates to a list
        coords = [float(x) for x in shapely_geometry.coords[0]]
        return GeoPoint(type="Point", coordinates=coords)
    elif isinstance(shapely_geometry, LineString):
        # For LineString, convert each coordinate tuple to a list
        coords = [[float(x) for x in coord] for coord in shapely_geometry.coords]
        return GeoLineString(type="LineString", coordinates=coords)
    elif isinstance(shapely_geometry, Polygon):
        # For Polygon, convert exterior coordinates
        coords = [[float(x) for x in coord] for coord in shapely_geometry.exterior.coords]
        return GeoPolygon(type="Polygon", coordinates=[coords])
    elif isinstance(shapely_geometry, MultiPoint):
        # For MultiPoint, convert each point's coordinates
        coords = [[float(x) for x in p.coords[0]] for p in shapely_geometry.geoms]
        return GeoMultiPoint(type="MultiPoint", coordinates=coords)
    elif isinstance(shapely_geometry, MultiLineString):
        # For MultiLineString, convert each line's coordinates
        coords = [[[float(x) for x in coord] for coord in line.coords] for line in shapely_geometry.geoms]
        return GeoMultiLineString(type="MultiLineString", coordinates=coords)
    elif isinstance(shapely_geometry, MultiPolygon):
        # For MultiPolygon, convert each polygon's exterior coordinates
        # Each polygon's coordinates need to be wrapped in an extra list
        coords = [[[[float(x) for x in coord] for coord in poly.exterior.coords]] for poly in shapely_geometry.geoms]
        return GeoMultiPolygon(type="MultiPolygon", coordinates=coords)
    else:
        raise ValueError(f"Unsupported geometry type: {type(shapely_geometry)}")


def geo_output(geo_data: models.GeoData):
    # Determine the geometry type from the geometry itself
    shapely_geometry = to_shape(geo_data.geometry)
    geometry_type = type(shapely_geometry).__name__
    
    return schemas.GeoOut(
        id=geo_data.id,
        name=geo_data.name,
        type=geometry_type,  # Use the actual geometry type
        geometry=wkb_to_geojson(geo_data.geometry)
    )


def create_geo_data(db: Session, geo_data: schemas.GeoCreate):
    shapely_geometry = shape(geo_data.geometry.model_dump())
    db_geo = models.GeoData(
            name=geo_data.name,
            type=geo_data.type,
            geometry=from_shape(shapely_geometry, srid=4326)
    )
    db.add(db_geo)
    db.commit()
    db.refresh(db_geo)
    
    return geo_output(db_geo)


def get_geo_data(db: Session, geo_data_id: int):
    geo_data = db.query(models.GeoData).filter(models.GeoData.id == geo_data_id).first()
    if not geo_data:
        raise HTTPException(status_code=404, detail="Geo data not found")
   
    return geo_output(geo_data)


def list_geo_data(db: Session):
    geo_data = db.query(models.GeoData).all()
    return [geo_output(geo) for geo in geo_data]


def delete_geo_data(db: Session, geo_data_id: int):
    geo_data = db.query(models.GeoData).filter(models.GeoData.id == geo_data_id).first()
    if not geo_data:
        raise HTTPException(status_code=404, detail="Geo data not found")
    db.delete(geo_data)
    db.commit()
    return {"message": "Geo data deleted successfully"}


def update_geo_data(db: Session, geo_data_id: int, geo_update: schemas.GeoCreate):
    db_geo = db.query(models.GeoData).filter(models.GeoData.id == geo_data_id).first()
    if not db_geo:
        raise HTTPException(status_code=404, detail="Geo data not found")
    db_geo.name = geo_update.name
    db_geo.type = geo_update.type
    db_geo.geometry = from_shape(shape(geo_update.geometry.model_dump()), srid=4326)
    db.commit()
    db.refresh(db_geo)
    return geo_output(db_geo)


