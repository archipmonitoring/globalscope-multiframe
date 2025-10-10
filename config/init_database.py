# config/init_database.py
# Ініціалізація бази даних PostgreSQL для платформи

from psycopg2 import connect
from dotenv import load_dotenv
import os

load_dotenv()

conn = connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'engineer',
    biometric_hash VARCHAR(256)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS chips (
    id SERIAL PRIMARY KEY,
    chip_id VARCHAR(50) UNIQUE NOT NULL,
    defect_rate FLOAT DEFAULT 0.0,
    power_usage FLOAT DEFAULT 0.0035,
    co2_impact FLOAT DEFAULT 0.20,
    yield_rate FLOAT DEFAULT 0.99
);
""")

conn.commit()
cur.close()
conn.close()

print("Database initialized! 🌌")