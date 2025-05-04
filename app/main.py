from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/geo-data/create/", response_model=schemas.GeoOut)
def create_geo_data(geo_data: schemas.GeoCreate, db: Session = Depends(database.get_db)):
    return crud.create_geo_data(db, geo_data)

@app.get("/geo-data/{geo_data_id}", response_model=schemas.GeoOut)
def get_geo_data(geo_data_id: int, db: Session = Depends(database.get_db)):
    return crud.get_geo_data(db, geo_data_id)

@app.get("/geo-data/list/", response_model=list[schemas.GeoOut])
def list_geo_data(db: Session = Depends(database.get_db)):
    return crud.list_geo_data(db)

@app.delete("/geo-data/{geo_data_id}", response_model=dict)
def delete_geo_data(geo_data_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_geo_data(db, geo_data_id)

@app.put("/geo-data/{geo_data_id}", response_model=schemas.GeoOut)
def update_geo_data(geo_data_id: int, geo_data: schemas.GeoCreate, db: Session = Depends(database.get_db)):
    return crud.update_geo_data(db, geo_data_id, geo_data)

