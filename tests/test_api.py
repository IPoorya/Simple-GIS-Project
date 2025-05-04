import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy.pool import StaticPool
import os

from app.main import app
from app.database import base, get_db
from app import models
from tests.test_config import TEST_DATABASE_URL, TEST_DB_NAME

# Create a connection to the default database to create the test database
default_db_url = TEST_DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
default_engine = create_engine(default_db_url)

# Test database setup
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database and tables"""
    # Drop test database if it exists and create a new one
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Close any open transaction
        # Terminate all connections to the test database
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
            AND pid <> pg_backend_pid();
        """))
        conn.execute(text("COMMIT"))
        # Drop the database if it exists
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text("COMMIT"))
        # Create a new database
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
    
    # Connect to the new database and enable PostGIS
    test_engine = create_engine(TEST_DATABASE_URL)
    with test_engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.execute(text("COMMIT"))
    
    # Create all tables
    base.metadata.create_all(bind=engine)
    yield
    # Clean up
    close_all_sessions()  # Close all SQLAlchemy sessions
    engine.dispose()  # Dispose of the engine
    test_engine.dispose()  # Dispose of the test engine
    
    # Drop all tables and database
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT"))
        # Terminate all connections again
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
            AND pid <> pg_backend_pid();
        """))
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text("COMMIT"))
    
    default_engine.dispose()  # Dispose of the default engine

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_create_geo_data_point(client):
    """Test creating a point geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [100.0, 0.0]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Point"
    assert data["type"] == "Point"
    assert data["geometry"]["type"] == "Point"
    assert data["geometry"]["coordinates"] == [100.0, 0.0]

def test_create_geo_data_linestring(client):
    """Test creating a linestring geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test LineString",
            "type": "LineString",
            "geometry": {
                "type": "LineString",
                "coordinates": [[100.0, 0.0], [101.0, 1.0]]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test LineString"
    assert data["type"] == "LineString"
    assert data["geometry"]["type"] == "LineString"
    assert data["geometry"]["coordinates"] == [[100.0, 0.0], [101.0, 1.0]]

def test_create_geo_data_polygon(client):
    """Test creating a polygon geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test Polygon",
            "type": "Polygon",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Polygon"
    assert data["type"] == "Polygon"
    assert data["geometry"]["type"] == "Polygon"
    assert data["geometry"]["coordinates"] == [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]

def test_create_geo_data_multipoint(client):
    """Test creating a multipoint geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test MultiPoint",
            "type": "MultiPoint",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [[100.0, 0.0], [101.0, 1.0]]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test MultiPoint"
    assert data["type"] == "MultiPoint"
    assert data["geometry"]["type"] == "MultiPoint"
    assert data["geometry"]["coordinates"] == [[100.0, 0.0], [101.0, 1.0]]

def test_create_geo_data_multilinestring(client):
    """Test creating a multilinestring geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test MultiLineString",
            "type": "MultiLineString",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [
                    [[100.0, 0.0], [101.0, 1.0]],
                    [[102.0, 2.0], [103.0, 3.0]]
                ]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test MultiLineString"
    assert data["type"] == "MultiLineString"
    assert data["geometry"]["type"] == "MultiLineString"
    assert data["geometry"]["coordinates"] == [
        [[100.0, 0.0], [101.0, 1.0]],
        [[102.0, 2.0], [103.0, 3.0]]
    ]

def test_create_geo_data_multipolygon(client):
    """Test creating a multipolygon geometry"""
    response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test MultiPolygon",
            "type": "MultiPolygon",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
                    [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
                ]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test MultiPolygon"
    assert data["type"] == "MultiPolygon"
    assert data["geometry"]["type"] == "MultiPolygon"
    # Use pytest.approx for comparing coordinates
    assert len(data["geometry"]["coordinates"]) == 2
    assert len(data["geometry"]["coordinates"][0][0]) == 5
    assert len(data["geometry"]["coordinates"][1][0]) == 5
    assert pytest.approx(data["geometry"]["coordinates"][0][0][0]) == [102.0, 2.0]
    assert pytest.approx(data["geometry"]["coordinates"][1][0][0]) == [100.0, 0.0]

def test_list_geo_data(client):
    """Test listing all geo data"""
    # First create some test data
    client.post(
        "/geo-data/create/",
        json={
            "name": "Test Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [100.0, 0.0]
            }
        }
    )
    
    response = client.get("/geo-data/list/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Point"

def test_get_geo_data(client):
    """Test getting a specific geo data entry"""
    # First create test data
    create_response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [100.0, 0.0]
            }
        }
    )
    geo_id = create_response.json()["id"]
    
    response = client.get(f"/geo-data/{geo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Point"
    assert data["id"] == geo_id

def test_delete_geo_data(client):
    """Test deleting a geo data entry"""
    # First create test data
    create_response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [100.0, 0.0]
            }
        }
    )
    geo_id = create_response.json()["id"]
    
    # Delete the entry
    response = client.delete(f"/geo-data/{geo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Geo data deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/geo-data/{geo_id}")
    assert get_response.status_code == 404

def test_update_geo_data(client):
    """Test updating a geo data entry"""
    # First create test data
    create_response = client.post(
        "/geo-data/create/",
        json={
            "name": "Test Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [100.0, 0.0]
            }
        }
    )
    geo_id = create_response.json()["id"]
    
    # Update the entry
    response = client.put(
        f"/geo-data/{geo_id}",
        json={
            "name": "Updated Point",
            "type": "Point",
            "geometry": {
                "type": "Point",
                "coordinates": [101.0, 1.0]
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Point"
    assert data["geometry"]["coordinates"] == [101.0, 1.0] 