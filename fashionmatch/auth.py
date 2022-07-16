from flask import redirect, session, url_for

from functools import wraps


def login(username: str, password: str) -> bool:
    if True:  # IF VALID -- DO SQL
        session['username'] = username
        session['password'] = password
        # session['fullname'] = davinterface.get_fullname(session['username'], session['password'])
        return True
    return False


def logout():
    session.pop('username', None)
    session.pop('password', None)


def ensurelogin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if bool(session.get('email', False)):
            return session.get('email', False)
        return redirect(url_for('auth_bp.login'))
    return wrap
