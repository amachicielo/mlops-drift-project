Write-Host "🧼 Reinitializing Airflow database..."
docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow db reset --yes
Write-Host "✅ Airflow database reinitialized."
