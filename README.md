# Simple GIS Project

A FastAPI-based Geographic Information System (GIS) application that allows you to store and manage various types of geographic data.

## Features

- Store and manage different types of geographic data:
  - Points
  - LineStrings
  - Polygons
  - MultiPoints
  - MultiLineStrings
  - MultiPolygons
- RESTful API endpoints for CRUD operations
- PostgreSQL/PostGIS database for spatial data storage
- Docker-based development environment

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd simple-gis-project
   ```

2. Create a `.env` file with the following variables:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`.

## API Endpoints

### Create Geo Data
```http
POST /geo-data/create/
Content-Type: application/json

{
    "name": "Test Point",
    "type": "Point",
    "geometry": {
        "type": "Point",
        "coordinates": [100.0, 0.0]
    }
}
```

### List Geo Data
```http
GET /geo-data/list/
```

### Get Geo Data
```http
GET /geo-data/{id}/
```

### Update Geo Data
```http
PUT /geo-data/{id}/
Content-Type: application/json

{
    "name": "Updated Point",
    "type": "Point",
    "geometry": {
        "type": "Point",
        "coordinates": [101.0, 1.0]
    }
}
```

### Delete Geo Data
```http
DELETE /geo-data/{id}/
```

## Supported Geometry Types

### Point
```json
{
    "type": "Point",
    "coordinates": [100.0, 0.0]
}
```

### LineString
```json
{
    "type": "LineString",
    "coordinates": [[100.0, 0.0], [101.0, 1.0]]
}
```

### Polygon
```json
{
    "type": "Polygon",
    "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
}
```

### MultiPoint
```json
{
    "type": "MultiPoint",
    "coordinates": [[100.0, 0.0], [101.0, 1.0]]
}
```

### MultiLineString
```json
{
    "type": "MultiLineString",
    "coordinates": [
        [[100.0, 0.0], [101.0, 1.0]],
        [[102.0, 2.0], [103.0, 3.0]]
    ]
}
```

### MultiPolygon
```json
{
    "type": "MultiPolygon",
    "coordinates": [
        [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
        [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
    ]
}
```

## Development

### Running Tests
```bash
docker exec -it simplegisproject-app-1 pytest -v tests/
```

### Project Structure
```
simple-gis-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_config.py
├── alembic/
│   └── versions/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Technologies Used

- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL/PostGIS - Database
- Docker - Containerization
- Pydantic - Data validation
- GeoJSON - Geographic data format
- Shapely - Geometric operations
- GeoAlchemy2 - Spatial database integration

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 

## Alembic Commands

To create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

To upgrade the database:
```bash
alembic upgrade head
``` 