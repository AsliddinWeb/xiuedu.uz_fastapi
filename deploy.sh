#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════"
echo "  XIU Edu — Production Deploy"
echo "═══════════════════════════════════════════════════"

cd "$(dirname "$0")"

if [ ! -f .env.prod ]; then
    echo "❌ .env.prod topilmadi!"
    exit 1
fi

echo "🔨 Building..."
docker compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
docker compose -f docker-compose.prod.yml up -d --build

echo "⏳ Kutamiz..."
sleep 10

echo "📊 Migrations..."
docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

echo "🌱 Seeding..."
for s in seed_data seed_home seed_leaders seed_about seed_applicants seed_structure seed_international seed_vacancies seed_contact seed_gallery update_real_data index_chat_content; do
    docker compose -f docker-compose.prod.yml exec -T backend python scripts/${s}.py 2>/dev/null || true
done

echo ""
echo "✅ Tayyor!"
docker compose -f docker-compose.prod.yml ps
echo ""
echo "Portlar: nginx=8100, backend=8114, redis=6382"
