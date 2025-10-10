# scripts/backup.sh
# Скрипт для щоденного резервного копіювання даних платформи

#!/bin/bash
set -e

echo "Backing up HoloMisha RealityForge..."

# Backup PostgreSQL
pg_dump -h postgres-service -U user -d holomisha > backup/holomisha_db_$(date +%Y%m%d).sql

# Backup Redis
docker exec redis-service redis-cli --scan --pattern "*" > backup/redis_data_$(date +%Y%m%d).json

# Backup logs
docker logs holomisha > backup/holomisha_logs_$(date +%Y%m%d).log

echo "Backup completed! 🌌"