Write-Host "🛑 Stopping all Airflow, API, and MLflow services..."

# Stops and removes containers, but keeps volumes and networks
docker-compose -f docker-compose.airflow.yml down

Write-Host "✅ All services have been stopped successfully."
