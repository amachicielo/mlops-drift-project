Write-Host "🧹 Deleting containers, networks, and volumes..."
docker-compose -f docker-compose.airflow.yml down -v

Write-Host "🔄 Rebuilding and starting services from scratch..."
docker-compose -f docker-compose.airflow.yml up --build

Write-Host "✅ Complete reconstruction."
