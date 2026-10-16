"""Shared helpers: time, auth, CSRF and the hifz analytics engine."""
import os
import secrets
from datetime import date, datetime, timedelta, timezone
from functools import wraps

from flask import abort, g, redirect, request, session, url_for

import db

BASE = os.path.dirname(os.path.abspath(__file__))
IST = timezone(timedelta(hours=5, minutes=30))

THEMES = [
    ('rawdat', 'Rawdat', '#2f968b'),
    ('emerald', 'Emerald', '#047857'),
    ('maroon', 'Maroon', '#701a34'),
    ('gold', 'Gold', '#b45309'),
    ('graphite', 'Graphite', '#334155'),
    ('amethyst', 'Amethyst', '#5c4d85'),
]


def now_ist():
    return datetime.now(IST)


def today_ist():
    return now_ist().date()


# ---------------------------------------------------------------- auth helpers
def current_user():
    if 'user' not in g:
        uid = session.get('uid')
        g.user = db.q('SELECT * FROM users WHERE id=?', (uid,), one=True) if uid else None
    return g.user


def login_required(*roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            u = current_user()
            if not u:
                return redirect(url_for('portal.login', next=request.full_path))
            if roles and u['role'] not in roles:
                abort(403)
            return fn(*a, **kw)
        return wrapper
    return deco


def csrf_token():
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_urlsafe(24)
    return session['_csrf']


# ---------------------------------------------------------------- hifz analytics
def hifz_summary(child_id, today=None):
    """Turn a child's tasmee' log into a mushaf map, pace, streak and a revision queue."""
    from quran import TOTAL_PAGES, juz_of_page, juz_pages
    today = today or today_ist()
    logs = db.q('SELECT * FROM hifz_logs WHERE child_id=? ORDER BY day', (child_id,))
    memorised, last_dhor, first_day = set(), {}, None
    days_active = set()
    for l in logs:
        d = date.fromisoformat(l['day'])
        first_day = first_day or d
        days_active.add(d)
        rng = range(min(l['page_from'], l['page_to']), max(l['page_from'], l['page_to']) + 1)
        if l['kind'] == 'sabaq':
            memorised.update(rng)
        else:
            for p in rng:
                j = juz_of_page(p)
                last_dhor[j] = max(last_dhor.get(j, d), d)
    juz = []
    for j in range(1, 31):
        a, b = juz_pages(j)
        done = sum(1 for p in range(a, b + 1) if p in memorised)
        total = b - a + 1
        juz.append(dict(n=j, done=done, total=total, pct=round(100 * done / total),
                        last_dhor=last_dhor.get(j), complete=done == total))
    # streak: consecutive school days (Mon–Sat) with a log, ending today or the last school day
    streak, d = 0, today
    if d not in days_active and d.weekday() != 6:
        d -= timedelta(days=1)
    while True:
        if d.weekday() == 6:
            d -= timedelta(days=1); continue
        if d in days_active:
            streak += 1; d -= timedelta(days=1)
        else:
            break
    window = today - timedelta(days=28)
    recent_new = set()
    for l in logs:
        if l['kind'] == 'sabaq' and date.fromisoformat(l['day']) > window:
            recent_new.update(range(min(l['page_from'], l['page_to']), max(l['page_from'], l['page_to']) + 1))
    per_week = round(len(recent_new) / 4, 1)
    remaining = TOTAL_PAGES - len(memorised)
    eta = (today + timedelta(weeks=remaining / per_week)) if per_week > 0 and remaining > 0 else None
    # revision queue: memorised juz (fully or partly), oldest revision first
    started = [j for j in juz if j['done']]
    queue = sorted(started, key=lambda j: (j['last_dhor'] or date(1900, 1, 1)))[:4]
    for j in queue:
        j['days_since'] = (today - j['last_dhor']).days if j['last_dhor'] else None
    recent = list(reversed(logs[-12:]))
    mistakes = [dict(day=l['day'], m=l['mistakes']) for l in logs if l['kind'] != 'sabaq'][-20:]
    return dict(pages=len(memorised), pct=round(100 * len(memorised) / TOTAL_PAGES, 1), juz=juz,
                juz_complete=sum(1 for j in juz if j['complete']), streak=streak, per_week=per_week,
                eta=eta, queue=queue, recent=recent, mistakes=mistakes, memorised=memorised,
                since=first_day)
