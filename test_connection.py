import psycopg2

try:
    conn = psycopg2.connect(
        host="portal-tesis-db-santoto.postgres.database.azure.com",
        database="portal_tesis",
        user="portaladmin",
        password="Cl4s3cl0ud2025",
        port=5432,
        sslmode="require"
    )
    print("✅ Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")