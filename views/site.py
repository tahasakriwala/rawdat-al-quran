import re
import secrets
from datetime import date

from flask import Blueprint, abort, redirect, render_template, request, url_for

import content as C
import db
from core import today_ist

bp = Blueprint('site', __name__)
EMAIL_RX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _albums():
    return sorted(C.data('albums'), key=lambda a: a['date'], reverse=True)


@bp.route('/')
def home():
    ex = C.data('media_extras')
    albums = _albums()
    upcoming = db.q("SELECT * FROM events WHERE day>=? ORDER BY day LIMIT 4", (today_ist().isoformat(),))
    return render_template('home.html', ex=ex, albums=albums[:8], newsletters=C.data('newsletters')[:4],
                           achievements=C.ACHIEVEMENTS, about=C.HOME_ABOUT, why=C.WHY, ayah=C.AYAH_14_24,
                           curriculum=C.CURRICULUM, day=C.DAY, upcoming=upcoming)


@bp.route('/about')
def about():
    ex = C.data('media_extras')
    return render_template('about.html', a=C.ABOUT, relax=C.RELAX, ayah=C.AYAH_14_24, ex=ex, achievements=C.ACHIEVEMENTS)


@bp.route('/campus')
def campus():
    ex = C.data('media_extras')
    return render_template('campus.html', text=C.CAMPUS, features=C.CAMPUS_FEATURES, ex=ex)


@bp.route('/people')
def people():
    return render_template('people.html', p=C.data('people'), msg=C.PRINCIPAL_MESSAGE)


@bp.route('/students')
def students():
    return render_template('students.html', groups=C.data('students'))


@bp.route('/curriculum')
def curriculum():
    return render_template('curriculum.html', tree=C.CURRICULUM, other=C.OTHER_INFO, ayah=C.AYAH_14_24, day=C.DAY,
                           ex=C.data('media_extras'))


@bp.route('/gallery')
def gallery():
    albums = _albums()
    cats = sorted({a['category'] for a in albums})
    years = sorted({a['date'][:4] for a in albums if a['date']}, reverse=True)
    return render_template('gallery.html', albums=albums, cats=cats, years=years)


@bp.route('/gallery/<slug>')
def album(slug):
    albums = _albums()
    a = next((x for x in albums if x['slug'] == slug), None) or abort(404)
    i = albums.index(a)
    return render_template('album.html', a=a, prev=albums[i - 1] if i else None,
                           nxt=albums[i + 1] if i + 1 < len(albums) else None)


@bp.route('/videos')
def videos():
    return render_template('videos.html', videos=C.data('videos'))


@bp.route('/audios')
def audios():
    return render_template('audios.html', tracks=C.data('audios'))


@bp.route('/newsletters')
def newsletters():
    return render_template('newsletters.html', items=C.data('newsletters'))


@bp.route('/newsletters/<slug>')
def newsletter(slug):
    n = next((x for x in C.data('newsletters') if x['slug'] == slug), None) or abort(404)
    return render_template('reader.html', title=n['title'], kicker='Monthly Newsletter', pages=n['pages'],
                           back=url_for('site.newsletters'), links=n.get('links', []))


@bp.route('/yearbooks')
def yearbooks():
    return render_template('yearbooks.html', items=C.data('yearbooks'), works=C.data('student_works'))


@bp.route('/yearbooks/<slug>')
def yearbook(slug):
    y = next((x for x in C.data('yearbooks') if x['slug'] == slug), None) or abort(404)
    return render_template('reader.html', title=f"{y['title']} {y['year']}", kicker='Year Book', pages=y['pages'],
                           back=url_for('site.yearbooks'), links=[])


@bp.route('/student-works/<slug>')
def student_work(slug):
    w = next((x for x in C.data('student_works') if x['slug'] == slug), None) or abort(404)
    return render_template('reader.html', title=w['title'], kicker='Student Works', pages=w['pages'],
                           back=url_for('site.yearbooks'), links=[])


@bp.route('/testimonials')
def testimonials():
    return render_template('testimonials.html', items=C.data('testimonials'))


@bp.route('/announcements')
def announcements():
    cls = request.args.get('class', 'all')
    rows = db.q("SELECT a.*, u.name AS author FROM announcements a LEFT JOIN users u ON u.id=a.author_id "
                "WHERE (?='all' OR a.class_slug IN (?, 'all')) ORDER BY pinned DESC, created DESC", (cls, cls))
    return render_template('announcements.html', rows=rows, cls=cls)


@bp.route('/events')
def events():
    t = today_ist()
    ym = request.args.get('m') or t.strftime('%Y-%m')
    try:
        y, m = map(int, ym.split('-'))
        first = date(y, m, 1)
    except ValueError:
        abort(404)
    upcoming = db.q("SELECT * FROM events WHERE day>=? ORDER BY day LIMIT 12", (t.isoformat(),))
    month_events = db.q("SELECT * FROM events WHERE substr(day,1,7)=? ORDER BY day", (first.strftime('%Y-%m'),))
    past = db.q("SELECT * FROM events WHERE day<? AND demo=0 ORDER BY day DESC", (t.isoformat(),))
    return render_template('events.html', first=first, upcoming=upcoming, month_events=month_events, past=past,
                           albums={a['slug']: a for a in C.data('albums')})


@bp.route('/admissions', methods=['GET', 'POST'])
def admissions():
    form, errors = {}, {}
    if request.method == 'POST':
        form = {k: (request.form.get(k) or '').strip() for k in
                ('parent_name', 'email', 'phone', 'child_name', 'dob', 'class_slug', 'academic_year', 'message')}
        for k in ('parent_name', 'email', 'phone', 'child_name', 'dob'):
            if not form[k]:
                errors[k] = 'Required'
        if form['email'] and not EMAIL_RX.match(form['email']):
            errors['email'] = 'Enter a valid email'
        if form['phone'] and len(re.sub(r'\D', '', form['phone'])) < 8:
            errors['phone'] = 'Enter a valid phone number'
        try:
            if form['dob']:
                date.fromisoformat(form['dob'])
        except ValueError:
            errors['dob'] = 'Use the date picker'
        if not errors:
            ref = 'RQK-' + secrets.token_hex(3).upper()
            db.x('INSERT INTO enquiries(ref,parent_name,email,phone,child_name,dob,class_slug,academic_year,message) '
                 'VALUES (?,?,?,?,?,?,?,?,?)', (ref, form['parent_name'], form['email'], form['phone'], form['child_name'],
                                               form['dob'], form['class_slug'], form['academic_year'], form['message']))
            return redirect(url_for('site.track', ref=ref, email=form['email'], new=1))
    t = today_ist()
    years = [f'{y}-{str(y + 1)[2:]}' for y in (t.year if t.month < 6 else t.year + 1, (t.year if t.month < 6 else t.year + 1) + 1)]
    return render_template('admissions.html', A=C.ADMISSION, form=form, errors=errors, years=years,
                           flyers=C.data('media_extras')['admission_flyers'])


@bp.route('/admissions/track')
def track():
    ref = (request.args.get('ref') or '').strip().upper()
    email = (request.args.get('email') or '').strip().lower()
    enq = None
    if ref and email:
        enq = db.q('SELECT * FROM enquiries WHERE ref=? AND lower(email)=?', (ref, email), one=True)
    return render_template('track.html', enq=enq, ref=ref, email=email, stages=db.ENQUIRY_STAGES,
                           closed=dict(db.ENQUIRY_CLOSED), searched=bool(ref), new=request.args.get('new'))


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    sent = False
    form, errors = {}, {}
    if request.method == 'POST':
        form = {k: (request.form.get(k) or '').strip() for k in ('name', 'email', 'subject', 'message')}
        for k in ('name', 'email', 'message'):
            if not form[k]:
                errors[k] = 'Required'
        if form.get('email') and not EMAIL_RX.match(form['email']):
            errors['email'] = 'Enter a valid email'
        if not errors:
            db.x('INSERT INTO contact_messages(name,email,subject,message) VALUES (?,?,?,?)',
                 (form['name'], form['email'], form['subject'], form['message']))
            sent, form = True, {}
    return render_template('contact.html', sent=sent, form=form, errors=errors)


@bp.route('/offline')
def offline():
    return render_template('offline.html')


@bp.route('/manifest.webmanifest')
def manifest():
    from flask import jsonify
    return jsonify({
        'name': 'Rawdat al-Quran al-Kareem', 'short_name': 'Rawdat', 'start_url': '/', 'display': 'standalone',
        'background_color': '#f6f1e6', 'theme_color': '#0c3c39', 'description': 'School, Hifz journey and family portal',
        'icons': [{'src': url_for('static', filename='img/icon-192.png'), 'sizes': '192x192', 'type': 'image/png'},
                  {'src': url_for('static', filename='img/icon-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}],
    })


@bp.route('/sw.js')
def sw():
    from flask import send_from_directory
    r = send_from_directory('static/js', 'sw.js', mimetype='application/javascript')
    r.headers['Cache-Control'] = 'no-cache'
    return r
