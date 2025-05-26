#!/usr/bin/env python
"""
Test database connection with the same parameters used by Django
"""
import os
import psycopg2

def test_connection():
    try:
        # Database connection parameters from secrets
        db_name = "core_medical"
        db_user = "django_user"
        db_password = "core_medical_pass_2024"
        db_host = "/cloudsql/molten-avenue-460900-a0:us-central1:core-medical-db"

        print(f"Testing connection to:")
        print(f"  Database: {db_name}")
        print(f"  User: {db_user}")
        print(f"  Host: {db_host}")

        # Try to connect
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
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

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

    return True

if __name__ == "__main__":
    test_connection()
