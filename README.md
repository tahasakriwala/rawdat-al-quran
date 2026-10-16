# Rawdat al-Quran al-Kareem — website, PWA & family portal

Designed and built by **Taha Sakriwala** · © 2026 Taha Sakriwala (code & design).

A Flask site for Rawdat al-Quran al-Kareem (Mahad al-Zahra · Aljamea-tus-Saifiyah), built on the
**Jaguar Type 01** look from the Anjuman-e-Saifee app (Inter, spaced capitals, hairlines, flat paper, one
accent colour, six colour themes, night mode) plus a Fatemi layer: keel arches, ivory marble paper, gold leaf,
khatam stars and a running Kanz inscription frieze. Arabic is set in **Kanz-al-Marjaan** and **AL-KANZ**.

## Run

From the `RQK` folder:

```bash
python3 -m venv .venv && .venv/bin/pip install -r rawdat/requirements.txt
.venv/bin/python rawdat/app.py   # http://127.0.0.1:5050
```

Restart the server after editing templates or Python files (it caches templates when not in debug mode;
`FLASK_DEBUG=1` reloads them automatically).

First run creates `instance/rawdat.sqlite3` and seeds it. Delete that file to reseed.

### Sample accounts (demo data only — remove before going live)

| Role    | Username | Password         |
|---------|----------|------------------|
| Office  | `admin`  | `rawdat-admin`   |
| Teacher | `teacher`| `rawdat-teacher` |
| Parent  | `parent` | `rawdat-parent`  |

Set `SHOW_DEMO_DATA=0` to hide the "Sample" badges, `RAWDAT_SECRET` to a long random string in production,
and `HIJRI_OFFSET_DAYS` if the Misri calendar ever needs a nudge.

## What's inside

**Public site** — Home (scroll-driven arch hero, ayah 14:24 word reveal, quick paths, live "A day at
Rawdat", album rail, newsletters, admissions with eligibility check) · About (founder, vision, R.E.L.A.X)
· Campus (36 photos) · People (principal, coordinators, searchable staff) · Students (class walls with
Arabic class names) · Curriculum (the Kalemah Tayyebah *Tree of Knowledge* that grows as you scroll) ·
Gallery (47 albums, 460+ photos, filters, lightbox) · Videos · 45 Arabic audio stories with a player ·
12 newsletters and 4 year books as page readers · Testimonials · Announcements by class · Calendar in
Gregorian + Misri Hijri · Admissions (eligibility by age on 1 June, six-step process, enquiry form →
reference number → public tracker) · Contact with map.

**Family portal** (`/portal`) — parent *Hifz journey*: progress ring, 30-juz mushaf map, all 604 pages,
streak, pace and projected khatm, murajaah queue (longest-unrevised juz first), tasmee' log, 12-week
attendance, leave requests, messages with the class teacher. **Teacher's desk** — register, tasmee'
logging by surah/page, leave approvals, class announcements. **School office** — admissions pipeline
(moving a card updates the family's tracker), inbox, announcements, calendar.

**Motion** — inertial smooth scrolling on mouse/trackpad, scroll scenes eased toward the scroll position,
GPU-composited hero (measured 60 fps with no dropped frames). Touch devices keep native momentum scrolling.

**Everywhere** — ⌘K / `/` search across pages, albums, staff, stories and curriculum; six colour themes
and night mode (saved per device); installable PWA with offline page; reduced-motion support.

## Content & media

- Text lives in `content.py`; lists (albums, people, students, newsletters, audios…) in `data/*.json`.
- Images and audio from rawdatalquran.com are optimised into `static/media/` (≈180 MB). The `|media`
  filter serves the local copy and falls back to the original URL, so year-book pages (not bundled) still load.
- **Official logos:** save the dome mark as `static/img/logo-mark.png` and the full crest as
  `static/img/logo-crest.png` — they replace the fallback crest everywhere. Then run
  `python scripts/make_icons.py` to rebuild the app icons.

## Layout

```
app.py          app factory, filters, error pages
core.py         time (IST), auth, CSRF, hifz analytics
content.py      school text + data loaders
db.py / seed.py SQLite schema and first-run seed
hijri.py        Misri (Fatemi) tabular Hijri calendar
quran.py        114 surahs, 30 juz, 604 pages
views/          site.py · portal.py · api.py
templates/      pages, partials/, portal/
static/         css/app.css · js/app.js · js/sw.js · fonts/ · img/ · media/
```

For production run behind a WSGI server, e.g. `gunicorn 'app:create_app()'`.

## Deploy to Render

The repo root is this `rawdat/` folder; `render.yaml` is a Render Blueprint.

1. Push this folder to a **private** GitHub repo (it contains student names and photos).
2. Render → **New → Blueprint** → pick the repo → **Apply**. It creates the web service
   (Starter plan, Singapore), a 1 GB persistent disk at `/var/data` for the SQLite database, and generates
   `RAWDAT_SECRET`, `ADMIN_PASSWORD`, `TEACHER_PASSWORD`, `PARENT_PASSWORD`.
3. Find those passwords under the service → **Environment**. Sign-in usernames are `admin`, `teacher`, `parent`.
4. Every `git push` redeploys automatically. The database on the disk survives deploys.

Environment variables: `RAWDAT_DB` (database path), `RAWDAT_SECRET`, `SHOW_DEMO_DATA` (`0` hides Sample
badges), `BEHIND_PROXY=1` and `SECURE_COOKIES=1` (HTTPS on Render), `HIJRI_OFFSET_DAYS`.
To reseed (e.g. after changing passwords), delete `/var/data/rawdat.sqlite3` from the service Shell and restart.
