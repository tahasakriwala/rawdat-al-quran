from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import content as C
import db
from core import current_user, hifz_summary, login_required, today_ist
from quran import juz_of_page, juz_pages, surah_list

bp = Blueprint('portal', __name__)
GRADES = ['Mumtaz', 'Jayyid Jiddan', 'Jayyid', 'Maqbool']


def _child_or_404(cid):
    u = current_user()
    c = db.q('SELECT * FROM children WHERE id=?', (cid,), one=True) or abort(404)
    if u['role'] == 'parent' and c['parent_id'] != u['id']:
        abort(403)
    if u['role'] == 'teacher' and c['class_slug'] != u['class_slug']:
        abort(403)
    return c


def _safe_next(n):
    return n if n and n.startswith('/') and not n.startswith('//') else None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        u = db.q('SELECT * FROM users WHERE username=?', ((request.form.get('username') or '').strip().lower(),), one=True)
        if u and check_password_hash(u['pw_hash'], request.form.get('password') or ''):
            csrf = session.get('_csrf')
            session.clear()
            session['uid'] = u['id']
            session['_csrf'] = csrf
            session.permanent = True
            return redirect(_safe_next(request.args.get('next')) or url_for('portal.home'))
        err = 'That username and password don’t match.'
    return render_template('portal/login.html', err=err, links=C.SCHOOL['links'])


@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('uid', None)
    return redirect(url_for('site.home'))


@bp.route('/')
@login_required()
def home():
    role = current_user()['role']
    return redirect(url_for({'parent': 'portal.family', 'teacher': 'portal.teacher', 'admin': 'portal.admin'}[role]))


# ---------------------------------------------------------------- parents
@bp.route('/family')
@login_required('parent')
def family():
    kids = db.q('SELECT * FROM children WHERE parent_id=?', (current_user()['id'],))
    if len(kids) == 1:
        return redirect(url_for('portal.child', cid=kids[0]['id']))
    cards = [dict(c=k, h=hifz_summary(k['id'])) for k in kids]
    return render_template('portal/family.html', cards=cards)


@bp.route('/child/<int:cid>')
@login_required('parent', 'teacher', 'admin')
def child(cid):
    c = _child_or_404(cid)
    h = hifz_summary(cid)
    t = today_ist()
    att = {r['day']: r['status'] for r in db.q('SELECT day,status FROM attendance WHERE child_id=? AND day>=?',
                                                (cid, (t - timedelta(days=84)).isoformat()))}
    days = [(t - timedelta(days=i)) for i in range(83, -1, -1)]
    present = sum(1 for v in att.values() if v == 'P')
    pct = round(100 * present / len(att)) if att else 0
    ann = db.q("SELECT * FROM announcements WHERE class_slug IN (?, 'all') ORDER BY pinned DESC, created DESC LIMIT 5", (c['class_slug'],))
    msgs = db.q('SELECT m.*, u.name AS sender, u.role AS srole FROM messages m JOIN users u ON u.id=m.sender_id WHERE child_id=? ORDER BY created', (cid,))
    leaves = db.q('SELECT * FROM leave_requests WHERE child_id=? ORDER BY created DESC LIMIT 5', (cid,))
    siblings = db.q('SELECT id,name FROM children WHERE parent_id=? AND id<>?', (c['parent_id'], cid)) if c['parent_id'] else []
    return render_template('portal/child.html', c=c, h=h, att=att, days=days, att_pct=pct, ann=ann, msgs=msgs,
                           leaves=leaves, siblings=siblings, newsletters=C.data('newsletters')[:3], links=C.SCHOOL['links'])


@bp.route('/child/<int:cid>/message', methods=['POST'])
@login_required('parent', 'teacher')
def message(cid):
    _child_or_404(cid)
    body = (request.form.get('body') or '').strip()
    if body:
        db.x('INSERT INTO messages(child_id,sender_id,body) VALUES (?,?,?)', (cid, current_user()['id'], body[:2000]))
    return redirect(url_for('portal.child', cid=cid) + '#messages')


@bp.route('/child/<int:cid>/leave', methods=['POST'])
@login_required('parent')
def leave(cid):
    _child_or_404(cid)
    f, t, r = request.form.get('from_day'), request.form.get('to_day'), (request.form.get('reason') or '').strip()
    try:
        if date.fromisoformat(t) < date.fromisoformat(f):
            f, t = t, f
    except (TypeError, ValueError):
        flash('Choose both dates for the leave request.')
        return redirect(url_for('portal.child', cid=cid) + '#leave')
    if r:
        db.x('INSERT INTO leave_requests(child_id,from_day,to_day,reason) VALUES (?,?,?,?)', (cid, f, t, r[:500]))
        flash('Leave request sent to the class teacher.')
    return redirect(url_for('portal.child', cid=cid) + '#leave')


# ---------------------------------------------------------------- teachers
@bp.route('/teacher')
@login_required('teacher')
def teacher():
    u = current_user()
    t = today_ist()
    day = request.args.get('day') or t.isoformat()
    kids = db.q('SELECT * FROM children WHERE class_slug=? ORDER BY name', (u['class_slug'],))
    att = {r['child_id']: r['status'] for r in db.q('SELECT child_id,status FROM attendance WHERE day=?', (day,))}
    roster = []
    for k in kids:
        h = hifz_summary(k['id'])
        last = db.q("SELECT * FROM hifz_logs WHERE child_id=? AND kind='sabaq' ORDER BY day DESC, id DESC LIMIT 1", (k['id'],), one=True)
        roster.append(dict(c=k, h=h, status=att.get(k['id']), last=last))
    leaves = db.q("SELECT l.*, c.name FROM leave_requests l JOIN children c ON c.id=l.child_id WHERE c.class_slug=? AND l.status='pending' ORDER BY l.created", (u['class_slug'],))
    return render_template('portal/teacher.html', roster=roster, day=day, leaves=leaves, grades=GRADES,
                           surahs=surah_list(), cls=u['class_slug'])


@bp.route('/teacher/attendance', methods=['POST'])
@login_required('teacher')
def attendance():
    u = current_user()
    day = request.form.get('day') or today_ist().isoformat()
    for k in db.q('SELECT id FROM children WHERE class_slug=?', (u['class_slug'],)):
        s = request.form.get(f's{k["id"]}')
        if s in ('P', 'A', 'L'):
            db.x('INSERT OR REPLACE INTO attendance(child_id,day,status) VALUES (?,?,?)', (k['id'], day, s))
    flash('Register saved.')
    return redirect(url_for('portal.teacher', day=day))


@bp.route('/teacher/log', methods=['POST'])
@login_required('teacher')
def log():
    cid = int(request.form['child_id'])
    _child_or_404(cid)
    try:
        a, b = int(request.form['page_from']), int(request.form['page_to'])
        assert 1 <= a <= 604 and 1 <= b <= 604
    except (KeyError, ValueError, AssertionError):
        flash('Pages must be between 1 and 604.')
        return redirect(url_for('portal.teacher'))
    kind = request.form.get('kind') if request.form.get('kind') in ('sabaq', 'sabaq_para', 'dhor') else 'sabaq'
    db.x('INSERT INTO hifz_logs(child_id,day,kind,page_from,page_to,mistakes,grade,note,teacher_id) VALUES (?,?,?,?,?,?,?,?,?)',
         (cid, request.form.get('day') or today_ist().isoformat(), kind, min(a, b), max(a, b),
          int(request.form.get('mistakes') or 0), request.form.get('grade'), (request.form.get('note') or '')[:300], current_user()['id']))
    flash('Tasmee’ recorded.')
    return redirect(url_for('portal.teacher') + f'#c{cid}')


@bp.route('/teacher/leave/<int:lid>', methods=['POST'])
@login_required('teacher')
def leave_decide(lid):
    l = db.q('SELECT * FROM leave_requests WHERE id=?', (lid,), one=True) or abort(404)
    _child_or_404(l['child_id'])
    st = 'approved' if request.form.get('ok') == '1' else 'declined'
    db.x('UPDATE leave_requests SET status=? WHERE id=?', (st, lid))
    if st == 'approved':
        d, end = date.fromisoformat(l['from_day']), date.fromisoformat(l['to_day'])
        while d <= end:
            db.x('INSERT OR REPLACE INTO attendance(child_id,day,status) VALUES (?,?,?)', (l['child_id'], d.isoformat(), 'L'))
            d += timedelta(days=1)
    return redirect(url_for('portal.teacher'))


@bp.route('/announce', methods=['POST'])
@login_required('teacher', 'admin')
def announce():
    u = current_user()
    title, body = (request.form.get('title') or '').strip(), (request.form.get('body') or '').strip()
    cls = u['class_slug'] if u['role'] == 'teacher' else (request.form.get('class_slug') or 'all')
    if title and body:
        db.x('INSERT INTO announcements(class_slug,title,body,pinned,author_id) VALUES (?,?,?,?,?)',
             (cls, title[:160], body[:3000], 1 if request.form.get('pinned') else 0, u['id']))
        flash('Announcement published.')
    return redirect(request.referrer or url_for('portal.home'))


# ---------------------------------------------------------------- admin
@bp.route('/admin')
@login_required('admin')
def admin():
    enq = db.q('SELECT * FROM enquiries ORDER BY created DESC')
    cols = [(k, label, [e for e in enq if e['status'] == k]) for k, label in db.ENQUIRY_STAGES + db.ENQUIRY_CLOSED]
    msgs = db.q('SELECT * FROM contact_messages ORDER BY created DESC LIMIT 30')
    ann = db.q('SELECT * FROM announcements ORDER BY created DESC LIMIT 20')
    ev = db.q('SELECT * FROM events WHERE day>=? ORDER BY day LIMIT 20', (today_ist().isoformat(),))
    stats = dict(enq=len(enq), new=sum(1 for e in enq if e['status'] == 'received'),
                 unread=sum(1 for m in msgs if not m['is_read']),
                 families=db.q("SELECT COUNT(*) n FROM users WHERE role='parent'", one=True)['n'])
    return render_template('portal/admin.html', cols=cols, msgs=msgs, ann=ann, ev=ev, stats=stats)


@bp.route('/admin/enquiry/<int:eid>', methods=['POST'])
@login_required('admin')
def enquiry_update(eid):
    st = request.form.get('status')
    valid = {k for k, _ in db.ENQUIRY_STAGES + db.ENQUIRY_CLOSED}
    if st in valid:
        db.x('UPDATE enquiries SET status=?, notes=coalesce(?, notes), updated=CURRENT_TIMESTAMP WHERE id=?',
             (st, request.form.get('notes') or None, eid))
    return redirect(url_for('portal.admin') + '#pipeline')


@bp.route('/admin/message/<int:mid>', methods=['POST'])
@login_required('admin')
def message_read(mid):
    db.x('UPDATE contact_messages SET is_read=1 WHERE id=?', (mid,))
    return redirect(url_for('portal.admin') + '#inbox')


@bp.route('/admin/event', methods=['POST'])
@login_required('admin')
def event_add():
    title, day = (request.form.get('title') or '').strip(), request.form.get('day')
    try:
        date.fromisoformat(day or '')
    except ValueError:
        flash('Pick a date for the event.')
        return redirect(url_for('portal.admin') + '#events')
    if title:
        db.x('INSERT INTO events(title,day,category,description) VALUES (?,?,?,?)',
             (title[:160], day, request.form.get('category') or 'School', (request.form.get('description') or '')[:1000]))
        flash('Event added to the calendar.')
    return redirect(url_for('portal.admin') + '#events')


@bp.route('/admin/announcement/<int:aid>/delete', methods=['POST'])
@login_required('admin')
def announcement_delete(aid):
    db.x('DELETE FROM announcements WHERE id=?', (aid,))
    return redirect(url_for('portal.admin') + '#announcements')


# Hifz map helpers for templates
@bp.app_template_global()
def juz_range(j):
    return juz_pages(j)


@bp.app_template_global()
def juz_for_page(p):
    return juz_of_page(p)
