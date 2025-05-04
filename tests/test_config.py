import os

# Test database configuration - using the main database container but with a different database name
TEST_DB_USER = os.getenv("POSTGRES_USER", "postgres")
TEST_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
TEST_DB_NAME = "test_db"  # Using a separate database name for tests
TEST_DB_PORT = os.getenv("POSTGRES_PORT", "5432")
TEST_DB_HOST = os.getenv("POSTGRES_HOST", "db")

TEST_DATABASE_URL = f"postgresql+psycopg2://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}" 