#!/bin/bash
# Test database connection and grant permissions

echo "Testing database connection and granting permissions..."

# Set up Cloud SQL proxy for local connection
./cloud_sql_proxy -instances=molten-avenue-460900-a0:us-central1:core-medical-db=tcp:5434 &
PROXY_PID=$!

# Wait for proxy to start
sleep 10

echo "Cloud SQL proxy started with PID: $PROXY_PID"

# Test connection with postgres user
echo "Testing connection with postgres user..."
PGPASSWORD="core_medical_pass_2024" psql -h 127.0.0.1 -p 5434 -U postgres -d core_medical -c "SELECT version();"

if [ $? -eq 0 ]; then
    echo "✅ Postgres connection successful!"

    # Grant permissions to django_user
    echo "Granting permissions to django_user..."
    PGPASSWORD="core_medical_pass_2024" psql -h 127.0.0.1 -p 5434 -U postgres -d core_medical << 'EOF'
GRANT ALL PRIVILEGES ON DATABASE core_medical TO django_user;
GRANT CREATE ON SCHEMA public TO django_user;
GRANT USAGE ON SCHEMA public TO django_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO django_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO django_user;
EOF

    if [ $? -eq 0 ]; then
        echo "✅ Permissions granted successfully!"

        # Test connection with django_user
        echo "Testing connection with django_user..."
        PGPASSWORD="core_medical_pass_2024" psql -h 127.0.0.1 -p 5434 -U django_user -d core_medical -c "SELECT current_user, current_database();"

        if [ $? -eq 0 ]; then
            echo "✅ Django user connection successful!"
        else
            echo "❌ Django user connection failed!"
        fi
    else
        echo "❌ Failed to grant permissions!"
    fi
else
    echo "❌ Postgres connection failed!"
fi

# Kill the proxy
kill $PROXY_PID
echo "Cloud SQL proxy stopped."
