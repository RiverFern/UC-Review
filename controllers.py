"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma


def get_user():
    return auth.current_user.get('id') if auth.current_user else None


url_signer = URLSigner(session)


@action('index')
@action.uses(db, auth, 'index.html')
def index():

    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url=URL('my_callback', signer=url_signer),
    )


@action('add_stats', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_stats.html')
def add_stats():
    form = Form(db.stats, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)


@action('edit_stats/<stats_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit_stats.html')
def edit_contact(stats_id=None):
    assert stats_id is not None
    p = db.stats[stats_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.stats, csrf_session=session, record=p, deletable=False, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('profile'))
    return dict(form=form)


@action('profile')
@action.uses(db, auth.user, 'profile.html')
def profile():

    stats = db(db.stats.student == get_user()).select().first()
    reviews = db(db.reviews.student == get_user()).select().first()

    return dict(stats=stats,
                reviews=reviews,
                load_stats_url=URL('load_stats', signer=url_signer),
                edit_stats_url=URL('edit_stats', signer=url_signer),
                )


@action('load_stats')
@action.uses(url_signer.verify(), db)
def load_stats():
    stats = db(db.stats.student == get_user()).select().as_list()
    return dict(stats=stats)


@action('edit_stats', method="POST")
@action.uses(url_signer.verify(), db)
def edit_stats():
    id = request.json.get("id")
    db(db.stats.id == id).update(
        school=request.json.get('school'),
        grad_year=request.json.get('grad_year'),
        major=request.json.get('major'),
        sat_score=request.json.get('sat_score'),
        act_score=request.json.get('act_score'),
        gpa=request.json.get('gpa'),
    )
    return dict()
