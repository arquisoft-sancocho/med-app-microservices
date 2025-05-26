#!/usr/bin/env python
"""
Test database connection using local proxy (127.0.0.1:5432)
"""
import psycopg2

def test_proxy_connection():
    try:
        # Database connection parameters for proxy
        db_name = "core_medical"
        db_user = "django_user"
        db_password = "core_medical_pass_2024"
        db_host = "127.0.0.1"
        db_port = "5432"

        print(f"Testing proxy connection to:")
        print(f"  Database: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Host: {db_host}")
        print(f"  Port: {db_port}")

        # Try to connect
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connection successful!")
        print(f"PostgreSQL version: {version[0]}")

        cursor.execute("SELECT current_user, current_database();")
        user_db = cursor.fetchone()
        print(f"Current user: {user_db[0]}")
        print(f"Current database: {user_db[1]}")

        # Test permissions by listing tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        print(f"Available tables: {len(tables)} found")
        for table in tables[:5]:  # Show first 5 tables
            print(f"  - {table[0]}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_proxy_connection()
