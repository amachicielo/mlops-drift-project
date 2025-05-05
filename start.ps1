Write-Host "🔄 Starting Airflow, API and MLflow..."

# Start services with Docker Compose (Airflow, Redis, Postgres, API, MLflow)
docker-compose -f docker-compose.airflow.yml up -d --build

Start-Sleep -Seconds 10

# Initialize the Airflow database if it is not initialized
Write-Host "🧱 Initializing the Airflow database..."
docker-compose -f docker-compose.airflow.yml exec airflow-webserver airflow db init

# Create admin user if it doesn't exist
Write-Host "👤 Creating admin user for Airflow..."
docker-compose -f docker-compose.airflow.yml exec airflow-webserver airflow users create `
  --username admin `
  --firstname Admin `
  --lastname User `
  --role Admin `
  --email admin@example.com `
  --password admin

Write-Host "✅ All set. Airflow available at: http://localhost:8080"
Write-Host "✅ Full stack up. To stop, use: .\stop.ps1"

