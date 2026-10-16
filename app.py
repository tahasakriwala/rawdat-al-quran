"""Rawdat al-Quran al-Kareem — school website, PWA and family portal.

Run:  python app.py           (http://127.0.0.1:5050)
Prod: gunicorn --preload app:app   (see render.yaml)
"""
import os
from datetime import date, datetime, timedelta

from flask import Flask, abort, request, session, url_for
from markupsafe import Markup, escape

import content
import db
from core import THEMES, csrf_token, current_user, now_ist, today_ist
from hijri import hijri_parts


# ---------------------------------------------------------------- app factory
def create_app(test_config=None):
    here = os.path.dirname(os.path.abspath(__file__))
    app = Flask('rawdat', root_path=here, instance_path=os.path.join(here, 'instance'), instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.environ.get('RAWDAT_SECRET', 'dev-change-me'),
        DATABASE=os.environ.get('RAWDAT_DB') or os.path.join(app.instance_path, 'rawdat.sqlite3'),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=os.environ.get('SECURE_COOKIES', '0') == '1',
        PERMANENT_SESSION_LIFETIME=timedelta(days=14),
        HIJRI_OFFSET_DAYS=int(os.environ.get('HIJRI_OFFSET_DAYS', 0)),
        SHOW_DEMO_DATA=os.environ.get('SHOW_DEMO_DATA', '1') == '1',
        SEND_FILE_MAX_AGE_DEFAULT=60 * 60 * 24 * 7,
    )
    if test_config:
        app.config.update(test_config)
    if os.environ.get('BEHIND_PROXY', '0') == '1':  # Render terminates HTTPS in front of the app
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE']) or '.', exist_ok=True)
    first_run = not os.path.exists(app.config['DATABASE'])
    db.init_db(app.config['DATABASE'])
    if first_run:
        import seed
        seed.run(app.config['DATABASE'])
    app.teardown_appcontext(db.close_db)

    from views.api import bp as api_bp
    from views.portal import bp as portal_bp
    from views.site import bp as site_bp
    app.register_blueprint(site_bp)
    app.register_blueprint(portal_bp, url_prefix='/portal')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.before_request
    def _csrf_protect():
        if request.method == 'POST':
            sent = request.form.get('_csrf') or request.headers.get('X-CSRF')
            if not sent or sent != session.get('_csrf'):
                abort(400, 'Form expired — please reload the page and try again.')

    @app.context_processor
    def _inject():
        t = today_ist()
        return dict(
            school=content.SCHOOL, user=current_user(), csrf_token=csrf_token, themes=THEMES,
            today=t, hijri=hijri_parts(t, app.config['HIJRI_OFFSET_DAYS']), classes=content.data('classes'),
            class_by_slug={c['slug']: c for c in content.data('classes')}, now=now_ist(),
            logo_mark=_logo('logo-mark.png'), logo_crest=_logo('logo-crest.png'),
        )

    def _logo(name):
        # Drop the official artwork into static/img/ and it is used everywhere; otherwise the cleaned crest.
        return url_for('static', filename='img/' + (name if content.media_exists('img/' + name) else 'crest.png'))

    @app.template_filter('media')
    def media_filter(url):
        """Serve a local optimised copy when we have it, otherwise the original URL."""
        rel = content.local_media_path(url)
        if rel and content.media_exists(rel):
            return url_for('static', filename=rel)
        return url or url_for('static', filename='img/crest.png')

    @app.template_filter('ar')
    def ar_filter(text):
        return Markup(f'<span class="ar" lang="ar" dir="rtl">{escape(text)}</span>')

    @app.template_filter('ardigits')
    def ardigits(n):
        return str(n).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))

    @app.template_filter('nicedate')
    def nicedate(v, fmt='%d %b %Y'):
        if not v:
            return ''
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v.replace(' ', 'T'))
            except ValueError:
                return v
        return v.strftime(fmt).lstrip('0')

    @app.template_filter('hijri')
    def hijri_filter(v, lang='en'):
        if isinstance(v, str):
            v = date.fromisoformat(v[:10])
        if isinstance(v, datetime):
            v = v.date()
        return hijri_parts(v, app.config['HIJRI_OFFSET_DAYS'])[lang]

    @app.template_filter('hday')
    def hday(v):
        h = hijri_parts(v, app.config['HIJRI_OFFSET_DAYS'])
        d = str(h['day']).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
        return f"{d} {h['month_ar'].split()[0]}" if h['day'] == 1 else d

    app.jinja_env.globals['timedelta'] = timedelta
    import math
    app.jinja_env.globals.update(cos=math.cos, sin=math.sin)

    @app.template_global()
    def asset(path):
        full = os.path.join(app.static_folder, path)
        v = int(os.path.getmtime(full)) if os.path.exists(full) else 0
        return url_for('static', filename=path, v=v)

    @app.template_filter('initials')
    def initials(name):
        parts = [p for p in name.replace('Shk ', '').replace('Ms ', '').replace('Mr ', '').replace('M ', '', 1).split() if p[:1].isalpha()]
        return ''.join(p[0] for p in parts[:2]).upper()

    @app.errorhandler(404)
    def _404(e):
        from flask import render_template
        return render_template('error.html', code=404, title='Page not found',
                               msg='This page has moved or never existed. Try the search, or head home.'), 404

    @app.errorhandler(403)
    def _403(e):
        from flask import render_template
        return render_template('error.html', code=403, title='Not for this account',
                               msg='Your account does not have access to this page.'), 403

    @app.errorhandler(400)
    def _400(e):
        from flask import render_template
        return render_template('error.html', code=400, title='Something went wrong',
                               msg=getattr(e, 'description', 'Bad request.')), 400

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5050)), debug=os.environ.get('FLASK_DEBUG') == '1')
