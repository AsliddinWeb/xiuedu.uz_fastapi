# XIU Edu v2 — xiuedu.uz

Premium private university website for **Xalqaro Innovatsion Universiteti**.
Modern stack, full multilingual support (uz/ru/en), built-in CMS, role-based admin panel, premium SEO.

---

## 🚀 Quick Start

```bash
git clone <repo-url>
cd XIUEDU.UZ_MAX
cp .env.example .env
# Edit .env (set SECRET_KEY, ADMIN_PASSWORD, etc.)

docker compose up --build
```

After containers come up:

```bash
# Apply migrations
docker compose exec backend alembic upgrade head

# Seed initial data (categories, sample news, static pages, SEO defaults)
docker compose exec backend python scripts/seed_data.py
```

Open:

| URL                                  | Description                          |
|--------------------------------------|--------------------------------------|
| http://localhost                     | Frontend (via nginx)                 |
| http://localhost:5176                | Frontend (direct dev)                |
| http://localhost:8014/api/docs       | FastAPI Swagger UI                   |
| http://localhost/admin               | Admin panel (use seeded credentials) |

Default admin: `admin@xiuedu.uz` / `ChangeMe123!` (change in `.env`).

---

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐
│   Vue 3 + Vite  │◄───┤  Nginx (80/443)  ├───►│  FastAPI     │
│   Tailwind      │    │  - SPA           │    │  + SQLAlchemy│
│   Pinia, i18n   │    │  - /api proxy    │    │  + Alembic   │
│   :5176         │    │  - 301 redirects │    │  :8014       │
└─────────────────┘    └──────────────────┘    └──────┬───────┘
                                                       │
                                ┌──────────────────────┴──────────┐
                                │                                  │
                          ┌─────▼──────┐                    ┌─────▼─────┐
                          │ PostgreSQL │                    │   Redis   │
                          │     16     │                    │ cache+RL  │
                          └────────────┘                    └───────────┘
```

| Layer       | Technology                                                      |
|-------------|------------------------------------------------------------------|
| Frontend    | Vue 3, Vite 5, Tailwind CSS 3, Pinia, Vue Router, vue-i18n       |
| Icons       | lucide-vue-next                                                  |
| Backend     | FastAPI, SQLAlchemy 2 (async), Alembic, Pydantic v2              |
| Database    | PostgreSQL 16                                                    |
| Cache / RL  | Redis 7 (slowapi)                                                |
| Auth        | JWT (access + refresh) + Redis blacklist                         |
| Reverse pxy | Nginx 1.27 (gzip, security headers, legacy 301 redirects)        |
| Container   | Docker Compose                                                   |

---

## 📁 Folder structure

```
XIUEDU.UZ_MAX/
├── backend/                FastAPI app
│   ├── app/
│   │   ├── models/         SQLAlchemy models
│   │   ├── schemas/        Pydantic schemas
│   │   ├── routers/        API routes (auth, news, pages, media, users, seo, stats, contact)
│   │   ├── services/       Business logic (auth, image processing)
│   │   ├── middleware/     CORS, logging, rate limit, cache
│   │   ├── utils/          security, deps, lang
│   │   └── main.py
│   ├── alembic/            Migrations
│   ├── tests/              Pytest suite
│   └── scripts/            seed_data.py
├── frontend/               Vue 3 SPA
│   └── src/
│       ├── api/            API clients
│       ├── components/     UI library (14+ components), layouts, sections
│       ├── composables/    useSeo, useReveal, useApi, useScrollAnimation, useToast
│       ├── i18n/           uz/ru/en (lazy)
│       ├── plugins/        analytics
│       ├── router/         Vue Router with role-based guards
│       ├── stores/         Pinia (auth, theme, language, toast)
│       ├── utils/          schema.js (Schema.org), roles.js
│       └── views/
│           ├── public/     Home, About, Faculties, News, Contact, ...
│           └── admin/      Dashboard, News, Pages, Media, Users, SEO
├── nginx/                  default.conf, redirects.conf
├── scripts/                backup.sh
├── .github/workflows/      ci.yml, deploy.yml
├── docker-compose.yml
├── .env.example
├── CHECKLIST.md            SEO + CWV audit
└── UPGRADE_GUIDE.md        v1 → v2 migration
```

---

## 🔐 Environment variables

| Variable                     | Description                              | Default                                           |
|-----------------------------|------------------------------------------|---------------------------------------------------|
| `POSTGRES_USER`             | Postgres user                            | `xiuedu`                                          |
| `POSTGRES_PASSWORD`         | Postgres password                        | `xiuedu_secret`                                   |
| `POSTGRES_DB`               | Postgres database                        | `xiuedu`                                          |
| `DATABASE_URL`              | Async SQLAlchemy URL                     | `postgresql+asyncpg://xiuedu:xiuedu_secret@db:5432/xiuedu` |
| `REDIS_URL`                 | Redis URL                                | `redis://redis:6379/0`                            |
| `SECRET_KEY`                | JWT secret (≥ 32 chars in production)    | `change-me-...`                                   |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access lifetime                    | `60`                                              |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh lifetime                     | `7`                                               |
| `ALLOWED_ORIGINS`           | Comma-separated CORS origins             | `http://localhost,http://localhost:5176,...`      |
| `SITE_URL`                  | Public site origin (used in sitemaps)    | `https://xiuedu.uz`                               |
| `SITE_NAME`                 | Display name                             | `Xalqaro Innovatsion Universiteti`                |
| `UPLOAD_DIR`                | Media upload directory inside container  | `/app/media`                                      |
| `MAX_UPLOAD_SIZE_MB`        | Max upload size                          | `20`                                              |
| `ADMIN_EMAIL`               | Bootstrap superadmin email               | `admin@xiuedu.uz`                                 |
| `ADMIN_PASSWORD`            | Bootstrap superadmin password            | `ChangeMe123!`                                    |
| `VITE_API_BASE_URL`         | Frontend API base URL                    | `http://localhost/api`                            |
| `VITE_GA4_ID`               | (optional) Google Analytics 4 ID         | empty (analytics disabled)                        |
| `VITE_YM_ID`                | (optional) Yandex Metrica counter ID     | empty                                             |

---

## 👤 Admin roles

| Role              | Permissions                                                              |
|-------------------|--------------------------------------------------------------------------|
| `superadmin`      | Full access. Cannot be deleted by other admins.                          |
| `admin`           | News, pages, media, users, SEO. No superadmin actions.                   |
| `content_manager` | News (full CRUD), media. Cannot edit pages or users.                     |
| `page_editor`     | Static pages (full CRUD), media. Cannot edit news or users.              |

Sidebar nav and route guards enforce these per route via `meta.roles`.

---

## 🌍 SEO features

- ✅ Per-route reactive `<title>`, meta description, OG, Twitter Card via [`useSeo`](frontend/src/composables/useSeo.js)
- ✅ Canonical link + hreflang (uz/ru/en + x-default) on every page
- ✅ Schema.org JSON-LD: `CollegeOrUniversity`, `WebSite`, `BreadcrumbList`, `NewsArticle`, `FAQPage`, `Event`, `Person`
- ✅ Sitemap index → static, pages, news (with `<image:image>` extensions, `xhtml:link` hreflang)
- ✅ Robots.txt with crawler rules + GPTBot block
- ✅ Nginx 301 legacy redirect map (~30 patterns)
- ✅ Multilingual CMS (per-language title, content, meta, OG image)
- ✅ Image WebP conversion + thumbnail/medium variants
- ✅ Web manifest (PWA basics)
- ✅ Adaptive theme-color (light/dark)

Full audit checklist: [CHECKLIST.md](CHECKLIST.md).

---

## ⚡ Performance targets

| Metric                          | Target            |
|---------------------------------|-------------------|
| Lighthouse Performance          | ≥ 90              |
| Lighthouse SEO                  | ≥ 95              |
| Lighthouse Accessibility        | ≥ 90              |
| Lighthouse Best Practices       | ≥ 95              |
| Initial JS (gzipped)            | < 150 KB          |
| Initial CSS (gzipped)           | < 30 KB           |
| LCP                             | < 2.5 s           |
| CLS                             | < 0.1             |
| INP                             | < 200 ms          |

Measure: `npm run build && npx lighthouse https://xiuedu.uz --view`.

Implementation:
- Vendor + route code splitting in [vite.config.js](frontend/vite.config.js)
- Lazy locale loading (uz eager, ru/en on-demand)
- LCP image preload, font preload
- `decoding="async"`, `loading="lazy"` defaults
- Cookie consent + analytics defer via `requestIdleCallback`

---

## 🧪 Testing

### Backend (pytest)

```bash
docker compose exec backend pytest -v
docker compose exec backend pytest --cov=app --cov-report=term-missing
```

In-memory SQLite, async fixtures, role-based auth headers. Coverage targets > 70%.

### Frontend (vitest)

```bash
docker compose exec frontend npm test
```

Tests for Pinia stores (theme, language), UI components (UIButton, UIBadge), schema helpers.

---

## 🔌 API documentation

Swagger UI: **http://localhost:8014/api/docs**

Key endpoints:

| Method | Path                              | Description                       |
|--------|-----------------------------------|-----------------------------------|
| POST   | `/api/auth/login`                 | Login → access + refresh tokens   |
| POST   | `/api/auth/refresh`               | Refresh access token              |
| GET    | `/api/auth/me`                    | Current user                      |
| GET    | `/api/news/?lang=uz&page=1`       | Public news list (paginated)      |
| GET    | `/api/news/{slug}?lang=uz`        | News detail (auto increments views) |
| GET    | `/api/pages/{slug}?lang=uz`       | Static page by slug               |
| POST   | `/api/admin/news/`                | Create news (CONTENT_MANAGER+)    |
| POST   | `/api/admin/media/upload`         | Upload media file                 |
| GET    | `/api/admin/stats/overview`       | Dashboard stats                   |
| GET    | `/api/sitemap.xml`                | Sitemap index                     |
| GET    | `/api/robots.txt`                 | Robots                            |
| POST   | `/api/contact`                    | Contact form submission           |

---

## 🚢 Deployment

1. **Server prerequisites:** Docker, Docker Compose v2, git.
2. Clone repo to `/opt/xiuedu`.
3. `cp .env.example .env` and edit production secrets.
4. `docker compose up -d --build`
5. `docker compose exec backend alembic upgrade head`
6. `docker compose exec backend python scripts/seed_data.py` (first time only)
7. Configure DNS A record → server IP.
8. Add HTTPS via Let's Encrypt (replace nginx default.conf with TLS variant or use traefik/caddy).

CI/CD:
- [.github/workflows/ci.yml](.github/workflows/ci.yml) — pytest + vitest + build + bundle size check
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml) — SSH deploy + alembic + health check + Telegram notification

Required secrets (Settings → Secrets):
- `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_PATH`
- `TG_BOT_TOKEN`, `TG_CHAT_ID`

Backups: `scripts/backup.sh` — daily `pg_dump`, 30-day rotation, optional S3 upload. Cron:
```
0 3 * * * /opt/xiuedu/scripts/backup.sh >> /var/log/xiuedu-backup.log 2>&1
```

---

## 🛠 Useful commands

```bash
# Logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart single service
docker compose restart backend

# New migration
docker compose exec backend alembic revision --autogenerate -m "msg"
docker compose exec backend alembic upgrade head

# Open Postgres shell
docker compose exec db psql -U xiuedu

# Run frontend build
docker compose exec frontend npm run build

# Backup now
./scripts/backup.sh
```

---

## 📚 Further reading

- [CHECKLIST.md](CHECKLIST.md) — SEO & Core Web Vitals audit
- [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) — migrating from old xiuedu.uz
