from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.database import base


class GeoData(base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    geometry = Column(Geometry(geometry_type="GEOMETRY", srid=4326))


