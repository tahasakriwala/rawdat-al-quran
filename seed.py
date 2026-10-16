"""First-run seed. Real school happenings come from data/albums.json; everything else is
SAMPLE data (flagged demo=1) so the portals have something to show. Delete instance/rawdat.sqlite3 to reseed.

Demo logins (change or delete before going live; on Render the passwords come from env vars):
    admin   / rawdat-admin
    teacher / rawdat-teacher
    parent  / rawdat-parent
"""
import json
import os
import random
import sqlite3
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DEMO_USERS = [  # passwords can be overridden with ADMIN_PASSWORD / TEACHER_PASSWORD / PARENT_PASSWORD
    ('admin', 'Admissions & Admin Office', 'admin', os.environ.get('ADMIN_PASSWORD', 'rawdat-admin'), None),
    ('teacher', 'Ms Tasneem Burhani', 'teacher', os.environ.get('TEACHER_PASSWORD', 'rawdat-teacher'), 'grade2'),
    ('parent', 'Demo Parent', 'parent', os.environ.get('PARENT_PASSWORD', 'rawdat-parent'), None),
]


def _school_days(start, end):
    d = start
    while d <= end:
        if d.weekday() != 6:  # Sunday off
            yield d
        d += timedelta(days=1)


def _hifz(con, child_id, teacher_id, start_juz, months, pace, rng, today):
    """Simulate a child memorising from Juz `start_juz` backwards (Amma first), with daily revision."""
    from quran import juz_of_page, juz_pages
    order = list(range(start_juz, 0, -1))
    queue = []
    for j in order:
        a, b = juz_pages(j)
        queue += list(range(a, b + 1))
    start = today - timedelta(days=30 * months)
    i = 0
    acc = 0.0
    done = []
    for d in _school_days(start, today):
        if rng.random() < 0.08:
            continue  # absent / holiday
        acc += max(0.0, rng.gauss(pace, pace * 0.4))  # pace = pages per school day
        n = int(acc)
        acc -= n
        new = queue[i:i + n]
        if new:
            con.execute('INSERT INTO hifz_logs(child_id,day,kind,page_from,page_to,mistakes,grade,teacher_id) VALUES (?,?,?,?,?,?,?,?)',
                        (child_id, d.isoformat(), 'sabaq', new[0], new[-1], rng.choice([0, 0, 1, 1, 2]),
                         rng.choice(['Mumtaz', 'Mumtaz', 'Jayyid Jiddan', 'Jayyid']), teacher_id))
            done += new; i += n
        if len(done) > 10:
            cur_j = juz_of_page(done[-1])
            sp = sorted(p for p in done[-10:] if juz_of_page(p) == cur_j)
            con.execute('INSERT INTO hifz_logs(child_id,day,kind,page_from,page_to,mistakes,grade,teacher_id) VALUES (?,?,?,?,?,?,?,?)',
                        (child_id, d.isoformat(), 'sabaq_para', sp[0], sp[-1], rng.choice([0, 1, 1, 2, 3]), 'Jayyid Jiddan', teacher_id))
        if len(done) > 25 and rng.random() < 0.7:
            j = juz_of_page(rng.choice(done[:-10]))
            pages = sorted(p for p in done if juz_of_page(p) == j)
            k = rng.randrange(0, max(1, len(pages) - 4))
            seg = pages[k:k + rng.choice([5, 10, 20])]
            con.execute('INSERT INTO hifz_logs(child_id,day,kind,page_from,page_to,mistakes,grade,teacher_id) VALUES (?,?,?,?,?,?,?,?)',
                        (child_id, d.isoformat(), 'dhor', seg[0], seg[-1], rng.choice([0, 1, 2, 2, 3, 4]), 'Jayyid', teacher_id))
        con.execute('INSERT OR IGNORE INTO attendance(child_id,day,status) VALUES (?,?,?)', (child_id, d.isoformat(), 'P'))
    for d in _school_days(today - timedelta(days=60), today):
        r = rng.random()
        if r < 0.04:
            con.execute('INSERT OR REPLACE INTO attendance(child_id,day,status) VALUES (?,?,?)', (child_id, d.isoformat(), 'A'))
        elif r < 0.08:
            con.execute('INSERT OR REPLACE INTO attendance(child_id,day,status) VALUES (?,?,?)', (child_id, d.isoformat(), 'L'))


def run(path):
    import sys
    sys.path.insert(0, BASE)
    rng = random.Random(1447)
    today = date.today()
    con = sqlite3.connect(path)
    ids = {}
    for u, name, role, pw, cls in DEMO_USERS:
        cur = con.execute('INSERT INTO users(username,name,role,pw_hash,class_slug) VALUES (?,?,?,?,?)',
                          (u, name, role, generate_password_hash(pw), cls))
        ids[u] = cur.lastrowid
    c1 = con.execute('INSERT INTO children(parent_id,name,class_slug,start_juz) VALUES (?,?,?,?)',
                     (ids['parent'], 'Sakina (sample)', 'grade2', 30)).lastrowid
    c2 = con.execute('INSERT INTO children(parent_id,name,class_slug,start_juz) VALUES (?,?,?,?)',
                     (ids['parent'], 'Husain (sample)', 'grade5', 30)).lastrowid
    # A few classmates so the teacher's register isn't lonely
    mates = ['Fatema', 'Burhanuddin', 'Zahra', 'Mustafa', 'Insiyah', 'Taher', 'Arwa', 'Ammar']
    mate_ids = [con.execute('INSERT INTO children(parent_id,name,class_slug) VALUES (NULL,?,?)', (f'{m} (sample)', 'grade2')).lastrowid for m in mates]
    _hifz(con, c1, ids['teacher'], 30, 14, 0.32, rng, today)
    _hifz(con, c2, ids['teacher'], 30, 30, 0.42, rng, today)
    for m in mate_ids:
        _hifz(con, m, ids['teacher'], 30, rng.randint(6, 16), rng.uniform(.18, .45), rng, today)

    # Real happenings, dated by their original posts
    albums = json.load(open(os.path.join(BASE, 'data', 'albums.json'), encoding='utf-8'))
    for a in albums:
        if a['date']:
            con.execute('INSERT INTO events(title,day,category,description,demo) VALUES (?,?,?,?,0)',
                        (a['title'], a['date'], a['category'], f"album:{a['slug']}"))
    # Sample upcoming items (clearly labelled)
    for off, title, cat, desc in [
        (3, 'Parent–Teacher Interaction', 'Academics', 'Meet your child’s class teacher to review the term.'),
        (9, 'Tilawat Musabaqat', 'Deen & Khidmat', 'Inter-class recitation competition.'),
        (16, 'EDU Field Trip — Grade 4', 'Trips & Outdoors', 'Experiential learning beyond the classroom.'),
        (23, 'Beach Clean-up', 'Learning Beyond Walls', 'Students and parents together at Chowpatty.'),
        (31, 'Annual Medal Ceremony', 'Celebrations & Learning', 'Celebrating the year’s Huffaz and achievers.'),
    ]:
        con.execute('INSERT INTO events(title,day,category,description,demo) VALUES (?,?,?,?,1)',
                    (title, (today + timedelta(days=off)).isoformat(), cat, desc))
    for cls, title, body, pin in [
        ('all', 'Welcome to the new Rawdat portal', 'Track hifz progress, attendance, announcements and newsletters in one place. Add this site to your home screen for a native app experience.', 1),
        ('grade2', 'Reading with my child — week 3', 'Please spend 15 minutes each evening listening to your child read. Share a line about it with the class teacher.', 0),
        ('grade5', 'Tilawat practice', 'Students should revise Surat al-Mulk with tarteel for the upcoming musabaqat.', 0),
        ('all', 'Morning Hifz class timing', 'Morning Hifz class runs 7:30 am to 8:45 am. Kindly ensure punctual arrival.', 0),
    ]:
        con.execute('INSERT INTO announcements(class_slug,title,body,pinned,author_id,demo) VALUES (?,?,?,?,?,1)',
                    (cls, title, body, pin, ids['admin']))
    con.execute('INSERT INTO messages(child_id,sender_id,body) VALUES (?,?,?)',
                (c1, ids['teacher'], 'Sakina recited her sabaq beautifully today, mashaAllah. Please revise the last 5 pages at home.'))
    con.commit()
    con.close()
