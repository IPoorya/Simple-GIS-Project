import os

# Test database configuration
TEST_DB_USER = "postgres"
TEST_DB_PASSWORD = "postgres"
TEST_DB_NAME = "test_db"
TEST_DB_PORT = "5432"
TEST_DB_HOST = "test_db"  # Changed from 'db' to 'test_db' to match the service name

TEST_DATABASE_URL = f"postgresql+psycopg2://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}" 