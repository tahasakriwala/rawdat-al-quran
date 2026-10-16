import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('parent','teacher','admin')),
  pw_hash TEXT NOT NULL, class_slug TEXT, email TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS children (
  id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES users(id), name TEXT NOT NULL,
  class_slug TEXT NOT NULL, hifz_goal_juz INTEGER DEFAULT 30, start_juz INTEGER DEFAULT 30
);
CREATE TABLE IF NOT EXISTS hifz_logs (
  id INTEGER PRIMARY KEY, child_id INTEGER REFERENCES children(id), day TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('sabaq','sabaq_para','dhor')),
  page_from INTEGER NOT NULL, page_to INTEGER NOT NULL, mistakes INTEGER DEFAULT 0,
  grade TEXT, note TEXT, teacher_id INTEGER REFERENCES users(id), created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS attendance (
  child_id INTEGER REFERENCES children(id), day TEXT NOT NULL, status TEXT NOT NULL CHECK (status IN ('P','A','L')),
  PRIMARY KEY (child_id, day)
);
CREATE TABLE IF NOT EXISTS announcements (
  id INTEGER PRIMARY KEY, class_slug TEXT DEFAULT 'all', title TEXT NOT NULL, body TEXT NOT NULL,
  pinned INTEGER DEFAULT 0, author_id INTEGER REFERENCES users(id), demo INTEGER DEFAULT 0,
  created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY, title TEXT NOT NULL, day TEXT NOT NULL, end_day TEXT, category TEXT,
  description TEXT, demo INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY, ref TEXT UNIQUE NOT NULL, parent_name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL,
  child_name TEXT NOT NULL, dob TEXT NOT NULL, class_slug TEXT, academic_year TEXT, message TEXT,
  status TEXT DEFAULT 'received', notes TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP, updated TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS contact_messages (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, subject TEXT, message TEXT NOT NULL,
  is_read INTEGER DEFAULT 0, created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS leave_requests (
  id INTEGER PRIMARY KEY, child_id INTEGER REFERENCES children(id), from_day TEXT NOT NULL, to_day TEXT NOT NULL,
  reason TEXT NOT NULL, status TEXT DEFAULT 'pending', created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY, child_id INTEGER REFERENCES children(id), sender_id INTEGER REFERENCES users(id),
  body TEXT NOT NULL, created TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_hifz_child ON hifz_logs(child_id, day);
"""

ENQUIRY_STAGES = [
    ('received', 'Enquiry received'),
    ('kit', 'Admission Kit shared'),
    ('applied', 'Application submitted'),
    ('interaction', 'Interaction scheduled'),
    ('decision', 'Decision pending'),
    ('offered', 'Admission granted'),
    ('confirmed', 'Seat confirmed'),
]
ENQUIRY_CLOSED = [('waitlist', 'Waitlisted'), ('declined', 'Not offered')]


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(_=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(path):
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.commit()
    con.close()


def q(sql, args=(), one=False):
    cur = get_db().execute(sql, args)
    rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows


def x(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid
