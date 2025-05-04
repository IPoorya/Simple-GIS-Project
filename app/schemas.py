from pydantic import BaseModel, ConfigDict
from typing import Union
from geojson_pydantic import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon

class GeoBase(BaseModel):
    name: str
    type: str
    model_config = ConfigDict(from_attributes=True)


class GeoCreate(GeoBase):
    geometry: Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]


class GeoOut(GeoBase):
    id: int
    geometry: Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]


