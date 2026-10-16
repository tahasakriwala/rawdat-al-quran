from datetime import date

from flask import Blueprint, jsonify, request, url_for

import content as C
from core import now_ist

bp = Blueprint('api', __name__)


@bp.route('/search-index')
def search_index():
    """Everything findable from the ⌘K palette."""
    idx = []
    add = lambda t, u, k, s='': idx.append(dict(t=t, u=u, k=k, s=s))  # noqa: E731
    for t, ep, s in [
        ('Home', 'site.home', 'A Dynamic Approach to Learning'), ('About us', 'site.about', 'Vision, belief, R.E.L.A.X'),
        ('Our campus', 'site.campus', 'Classrooms, library, corridors'), ('Our people', 'site.people', 'Principal, coordinators, staff'),
        ('Our students', 'site.students', 'Class walls, JKG to Grade 10'), ('Curriculum', 'site.curriculum', 'The Tree of Knowledge'),
        ('Photo gallery', 'site.gallery', '47 albums'), ('Videos', 'site.videos', ''), ('Arabic audio stories', 'site.audios', 'حكايات'),
        ('Newsletters', 'site.newsletters', 'Monthly'), ('Year books', 'site.yearbooks', 'Student works'),
        ('Admissions', 'site.admissions', 'Eligibility, process, enquire'), ('Track application', 'site.track', 'Reference number'),
        ('Announcements', 'site.announcements', 'By class'), ('Events & calendar', 'site.events', 'Hijri and Gregorian'),
        ('Testimonials', 'site.testimonials', 'Parents'), ('Contact & visit', 'site.contact', 'Warden Road, Mumbai'),
        ('Family portal login', 'portal.login', 'Parents, teachers'),
    ]:
        add(t, url_for(ep), 'Page', s)
    for k, v in C.SCHOOL['links'].items():
        add({'fees': 'Pay fees online', 'reports': 'Report cards login', 'webmail': 'Staff webmail',
             'tahfeez_portal': 'Tahfeez parent portal'}[k], v, 'Link')
    for a in C.data('albums'):
        add(a['title'], url_for('site.album', slug=a['slug']), 'Album', f"{a['category']} · {a['date'][:4]}")
    for n in C.data('newsletters'):
        add(f"Newsletter — {n['title']}", url_for('site.newsletter', slug=n['slug']), 'Newsletter')
    for y in C.data('yearbooks'):
        add(f"{y['title']} {y['year']}", url_for('site.yearbook', slug=y['slug']), 'Year book')
    for t in C.data('audios'):
        add(t['title'], url_for('site.audios') + f"#t{t['n']}", 'Audio story', f"#{t['n']}")
    p = C.data('people')
    for person in [p['principal']] + p['hods'] + p['male'] + p['female']:
        add(person['name'], url_for('site.people') + '#staff', 'Staff', person.get('role', ''))
    for c in C.CURRICULUM:
        for i in c['items']:
            add(i, url_for('site.curriculum') + f"#{c['key']}", 'Curriculum', c['title'])
    return jsonify(idx)


@bp.route('/now')
def now():
    """What is happening at Rawdat right now (Mumbai time)."""
    n = now_ist()
    hm = n.strftime('%H:%M')
    cur = None
    if n.weekday() != 6:
        for a, b, title, ar, desc in C.DAY:
            if a <= hm < b:
                cur = dict(title=title, ar=ar, desc=desc, until=b)
    return jsonify(time=hm, weekday=n.strftime('%A'), current=cur, open=n.weekday() != 6 and '07:30' <= hm < '15:10')


@bp.route('/eligibility')
def eligibility():
    """Age on 1 June of the academic year → class. JKG from four years and above."""
    try:
        dob = date.fromisoformat(request.args['dob'])
        start_year = int(request.args.get('year', '')[:4] or now_ist().year)
    except (KeyError, ValueError):
        return jsonify(error='Enter a valid date of birth'), 400
    ref = date(start_year, 6, 1)
    years = ref.year - dob.year - ((ref.month, ref.day) < (dob.month, dob.day))
    months = (ref.year - dob.year) * 12 + ref.month - dob.month - (ref.day < dob.day)
    classes = C.data('classes')
    idx = years - 4
    if idx < 0:
        return jsonify(age_years=years, age_months=months % 12, eligible=False,
                       message=f'Too young for {start_year}-{str(start_year + 1)[2:]}: JKG starts at four years on 1st June.',
                       next_year=dob.year + 4)
    if idx >= len(classes):
        return jsonify(age_years=years, age_months=months % 12, eligible=False,
                       message='Beyond the age range Rawdat admits into. Please contact the Admissions Office.')
    c = classes[idx]
    return jsonify(age_years=years, age_months=months % 12, eligible=True, cls=c,
                   message=f"Age-appropriate class: {c['label']} ({c['name']})")
