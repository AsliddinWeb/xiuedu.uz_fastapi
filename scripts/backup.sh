#!/usr/bin/env bash
# Daily PostgreSQL backup for XIU Edu v2.
#
# Usage: run from project root or via cron:
#   0 3 * * * /opt/xiuedu/scripts/backup.sh >> /var/log/xiuedu-backup.log 2>&1

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backups/xiuedu}"
KEEP_DAYS="${KEEP_DAYS:-30}"
COMPOSE_PROJECT="${COMPOSE_PROJECT:-xiuedu}"
DB_SERVICE="${DB_SERVICE:-db}"
DB_USER="${POSTGRES_USER:-xiuedu}"
DB_NAME="${POSTGRES_DB:-xiuedu}"

mkdir -p "$BACKUP_DIR"

DATE=$(date +%F-%H%M)
DEST="$BACKUP_DIR/xiuedu-$DATE.sql.gz"

echo "[$(date -Iseconds)] Backing up to $DEST"
docker compose exec -T "$DB_SERVICE" pg_dump -U "$DB_USER" -d "$DB_NAME" \
    --no-owner --no-acl --clean --if-exists \
  | gzip -9 > "$DEST"

# Verify size > 0
if [ ! -s "$DEST" ]; then
  echo "ERROR: backup file is empty" >&2
  rm -f "$DEST"
  exit 1
fi

echo "Backup OK: $(du -h "$DEST" | cut -f1)"

# Rotate: delete files older than KEEP_DAYS
find "$BACKUP_DIR" -name "xiuedu-*.sql.gz" -mtime +"$KEEP_DAYS" -delete
echo "Rotation: kept last $KEEP_DAYS days"

# Optional: upload to S3 if AWS_BUCKET set
if [ -n "${AWS_BUCKET:-}" ]; then
  if command -v aws >/dev/null 2>&1; then
    aws s3 cp "$DEST" "s3://$AWS_BUCKET/xiuedu/$(basename "$DEST")" \
      --storage-class STANDARD_IA
    echo "Uploaded to s3://$AWS_BUCKET/xiuedu/"
  else
    echo "AWS CLI not installed, skipping S3 upload"
  fi
fi

echo "[$(date -Iseconds)] Done."
