# test_db.py
import os
from sqlalchemy import create_engine

# Tomamos la DB del entorno
db_url = os.environ.get("SQLALCHEMY_DATABASE_URI", "mysql+pymysql://openecoe:openecoe@db:3306/openECOE_dev")

engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1").scalar()
        print(f"✅ Conexión correcta a la base de datos, resultado: {result}")
except Exception as e:
    print("❌ Error conectando a la base de datos:", e)
