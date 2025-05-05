Write-Host "🔁 Restarting all services..."

# Stop and remove containers
docker-compose -f docker-compose.airflow.yml down

# Start and build the containers again
docker-compose -f docker-compose.airflow.yml up --build

Write-Host "✅ All services have been restarted."
