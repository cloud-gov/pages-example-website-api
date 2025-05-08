#!/bin/bash

#Exit script if any command failure occurs
set -e

echo "Building and starting Docker containers..."
docker compose build
docker compose up -d

echo "Waiting for PostgreSQL database to be ready..."
sleep 5 #A small wait time for the database to initialize

echo "Creating table and injecting mock data..."
docker exec -i pg-database psql -U pguser -d app_db << EOF
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id serial PRIMARY KEY,
    name text NOT NULL,
    created_on timestamptz DEFAULT CURRENT_TIMESTAMP
    );

    INSERT INTO users (name)
    SELECT 'User' || i
    FROM generate_series(1, 10) as i;

    SELECT COUNT(*) AS total_users FROM users;
EOF

    echo "Setup completed successfully!"