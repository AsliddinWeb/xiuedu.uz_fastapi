# XIU Edu v1 → v2 Upgrade Guide

How to migrate content from the legacy `xiuedu.uz` site to the new v2 stack.

---

## 1. What changes

| Aspect            | v1 (legacy)              | v2 (this repo)                              |
|-------------------|--------------------------|---------------------------------------------|
| Stack             | PHP / WordPress-like CMS | FastAPI + Vue 3 + PostgreSQL                |
| URL pattern       | `/uz/news/...`           | `/news/...` (lang via `?lang=` query)       |
| Multilingual      | Per-page duplicates      | Single record × 3 language fields           |
| Sitemap           | Static                   | Dynamic split (static/pages/news)           |
| SEO meta          | Often empty              | Per-language `meta_title` + `meta_description` |
| Image processing  | Manual                   | Auto WebP + thumbnail + medium variants     |
| Auth              | Session cookie           | JWT (access + refresh) + Redis blacklist    |

---

## 2. Pre-flight

```bash
git clone <repo-url>
cd XIUEDU.UZ_MAX
cp .env.example .env
# Edit .env: set DATABASE_URL, SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
docker compose up -d --build
docker compose exec backend alembic upgrade head
```

Verify the API is up: `curl http://localhost:8014/api/health`.

---

## 3. Export legacy content

### News

Export from old admin or directly from the old database:

```sql
-- Example: dump WordPress-style posts
SELECT id, post_name AS slug, post_title, post_content, post_excerpt,
       post_date, post_status
FROM wp_posts WHERE post_type = 'post'
INTO OUTFILE '/tmp/legacy_news.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\'
LINES TERMINATED BY '\n';
```

If your CMS exports JSON, dump as `legacy_news.json` with shape:

```json
[
  {
    "slug": "yangi-akademik-yil",
    "lang": "uz",
    "title": "Yangi akademik yil",
    "excerpt": "...",
    "body": "<p>...</p>",
    "cover_image": "https://old.xiuedu.uz/wp-content/uploads/...",
    "category": "yangiliklar",
    "published_at": "2024-09-01T08:00:00Z"
  }
]
```

### Pages

```json
[
  {
    "slug": "biz-haqimizda",
    "translations": {
      "uz": {"title": "Biz haqimizda", "content": "<p>...</p>"},
      "ru": {"title": "О нас",        "content": "<p>...</p>"},
      "en": {"title": "About us",     "content": "<p>...</p>"}
    }
  }
]
```

### Media

`rsync` the old `wp-content/uploads/` (or equivalent) to a temp directory.

---

## 4. Run the import

A skeleton import script lives at `backend/scripts/seed_data.py`. Adapt it for your data, or use the API directly:

```bash
# Login to get a token
TOKEN=$(curl -s -X POST http://localhost:8014/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@xiuedu.uz","password":"ChangeMe123!"}' \
  | jq -r .access_token)

# Create a category
curl -X POST http://localhost:8014/api/admin/news/categories/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"slug":"yangiliklar","name_uz":"Yangiliklar","name_ru":"Новости","name_en":"News"}'

# Create a news article
curl -X POST http://localhost:8014/api/admin/news/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @article.json
```

Pseudo-code for a Python import:

```python
import asyncio, json, httpx

API   = "http://localhost:8014/api"
TOKEN = "..."

async def main():
    data = json.load(open("legacy_news_grouped.json"))
    async with httpx.AsyncClient(base_url=API,
                                 headers={"Authorization": f"Bearer {TOKEN}"}) as c:
        for item in data:
            payload = {
                "slug":       item["slug"],
                "title_uz":   item["uz"]["title"],
                "title_ru":   item["ru"]["title"],
                "title_en":   item["en"]["title"],
                "body_uz":    item["uz"]["body"],
                "body_ru":    item["ru"]["body"],
                "body_en":    item["en"]["body"],
                "excerpt_uz": item["uz"]["excerpt"],
                "excerpt_ru": item["ru"]["excerpt"],
                "excerpt_en": item["en"]["excerpt"],
                "category_id": item.get("category_id"),
                "cover_image": item.get("cover_image"),
                "is_published": True,
                "published_at": item["published_at"]
            }
            r = await c.post("/admin/news/", json=payload)
            print(r.status_code, item["slug"])

asyncio.run(main())
```

Tip: group your three single-language exports into one record per slug before posting.

---

## 5. Migrate media files

```bash
# Inside backend container
docker compose exec backend bash
mkdir -p /app/media/legacy
# Copy from your local export
# (run from host)
docker cp ./old-uploads xiuedu_backend:/app/media/legacy
```

Then update each news record's `cover_image` to point to `/media/legacy/...` (or re-upload via `POST /api/admin/media/upload` for WebP conversion).

---

## 6. URL redirects

The old URL scheme is mapped to v2 paths in [nginx/redirects.conf](nginx/redirects.conf). Edit that file if you have additional patterns. After editing:

```bash
docker compose restart nginx
```

Test:
```bash
curl -I http://localhost/uz/news/article-slug
# HTTP/1.1 301 Moved Permanently
# Location: /news/article-slug
```

Common patterns already covered:

| Old path                                | New path                |
|-----------------------------------------|-------------------------|
| `/uz/news/<slug>`                       | `/news/<slug>`          |
| `/ru/news/<slug>`                       | `/news/<slug>`          |
| `/en/news/<slug>`                       | `/news/<slug>`          |
| `/uz/page/<slug>`                       | `/p/<slug>`             |
| `/yangiliklar/<slug>`                   | `/news/<slug>`          |
| `/biz-haqimizda`, `/o-nas`, `/about-us` | `/about`                |
| `/rahbariyat`, `/rukovodstvo`           | `/leadership`           |
| `/fakultetlar`, `/fakultety`            | `/faculties`            |
| `/abituriyent`, `/postupayushchim`      | `/applicants`           |
| `/aloqa`, `/kontakty`                   | `/contact`              |
| `/galereya`                             | `/gallery`              |
| `/vakansiya`, `/vakansii`               | `/careers`              |

---

## 7. Post-migration checklist

- [ ] All redirects return 301 (test 10–20 important URLs)
- [ ] Sitemap submitted to Google Search Console & Yandex Webmaster
- [ ] Old domain → new domain DNS cutover scheduled
- [ ] Each language version of each article verified (`?lang=ru`, `?lang=en`)
- [ ] Cover images render and have `alt` attributes
- [ ] Search Console Sitemaps panel shows `Success` for all 3 sub-sitemaps
- [ ] Lighthouse score on key pages ≥ 90
- [ ] 404s monitored for first 7 days; add redirects as needed
- [ ] GA4 / Yandex Metrica counter IDs set in `.env` and consent banner working
- [ ] Database backup cron job verified (`./scripts/backup.sh`)

---

## 8. Rollback plan

If something goes wrong:

```bash
# Restore from latest backup
gunzip -c /var/backups/xiuedu/xiuedu-2026-04-07.sql.gz \
  | docker compose exec -T db psql -U xiuedu -d xiuedu

# Or roll back code
git checkout <previous-tag>
docker compose up -d --build
```

Keep DNS TTL low (300s) during the cutover so you can flip back quickly.
