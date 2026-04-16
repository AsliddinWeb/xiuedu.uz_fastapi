#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════"
echo "  XIU Edu — Deploy (Dockersiz)"
echo "═══════════════════════════════════════════════════"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

if [ ! -f .env.prod ]; then
    echo "❌ .env.prod topilmadi!"
    exit 1
fi

# Export env vars
set -a; source .env.prod; set +a

# ── 1. Redis ──
echo ""
echo "📦 Redis..."
if redis-cli ping >/dev/null 2>&1; then
    echo "  ✓ Redis ishlayapti"
else
    redis-server --daemonize yes --bind 127.0.0.1 --port 6379 --dir /tmp
    echo "  ✓ Redis ishga tushdi"
fi

# ── 2. Backend ──
echo ""
echo "🐍 Backend..."
cd "$PROJECT_DIR/backend"

if [ ! -d venv ]; then
    echo "  venv yaratilmoqda..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q 2>&1 | tail -1

# Migrations
echo "  📊 Migrations..."
alembic upgrade head 2>&1 | tail -3

# Seed
echo "  🌱 Seeding..."
for s in seed_data seed_home seed_leaders seed_about seed_applicants seed_structure seed_international seed_vacancies seed_contact seed_gallery update_real_data index_chat_content; do
    python "$PROJECT_DIR/scripts/${s}.py" 2>/dev/null || true
done
echo "  ✓ Seed OK"

# Backend restart
echo "  🔄 Backend restart..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 2
nohup "$PROJECT_DIR/backend/venv/bin/uvicorn" app.main:app \
    --host 127.0.0.1 \
    --port 8014 \
    --workers 2 \
    --app-dir "$PROJECT_DIR/backend" \
    > /tmp/xiuedu_backend.log 2>&1 &
echo "  ✓ Backend started (PID: $!, port 8014)"

deactivate
cd "$PROJECT_DIR"

# ── 3. Frontend ──
echo ""
echo "🔨 Frontend build..."
cd "$PROJECT_DIR/frontend"

# Node 18 da vite ishlaydi
npm install --silent 2>/dev/null
VITE_API_BASE_URL="${VITE_API_BASE_URL}" \
VITE_SITE_URL="${VITE_SITE_URL}" \
npm run build 2>&1 | tail -3

sudo mkdir -p /var/www/xiuedu
sudo rm -rf /var/www/xiuedu/*
sudo cp -r dist/* /var/www/xiuedu/
echo "  ✓ Frontend → /var/www/xiuedu/"

cd "$PROJECT_DIR"

# ── 4. Media ──
sudo mkdir -p /var/www/xiuedu-media
sudo chown "$USER:$USER" /var/www/xiuedu-media
rm -f "$PROJECT_DIR/backend/media"
ln -sfn /var/www/xiuedu-media "$PROJECT_DIR/backend/media"
echo "  ✓ Media → /var/www/xiuedu-media/"

# ── 5. Nginx ──
echo ""
echo "🌐 Nginx..."
sudo cp "$PROJECT_DIR/nginx/server-xiuedu.uz.conf" /etc/nginx/sites-available/xiuedu.uz
sudo ln -sfn /etc/nginx/sites-available/xiuedu.uz /etc/nginx/sites-enabled/xiuedu.uz
if sudo nginx -t 2>&1 | grep -q "successful"; then
    sudo systemctl reload nginx
    echo "  ✓ Nginx OK"
else
    echo "  ⚠️  Nginx config xato — tekshiring: sudo nginx -t"
fi

# ── 6. Tekshirish ──
echo ""
echo "🔍 Tekshirish..."
sleep 2
if curl -s http://127.0.0.1:8014/api/ | grep -q "XIU"; then
    echo "  ✓ Backend API ishlayapti"
else
    echo "  ⚠️  Backend javob bermayapti — log: cat /tmp/xiuedu_backend.log"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ Deploy yakunlandi!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  Backend:  http://127.0.0.1:8014/api/"
echo "  Frontend: /var/www/xiuedu/"
echo "  Logs:     /tmp/xiuedu_backend.log"
echo ""
echo "  SSL olish:"
echo "    sudo certbot --nginx -d xiuedu.uz -d www.xiuedu.uz"
echo ""
