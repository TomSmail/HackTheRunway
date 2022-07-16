from flask import redirect, session, url_for

from functools import wraps


def ensurelogin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if bool(session.get('email', False)):
            return session.get('email', False)
        return redirect(url_for('account_bp.login'))
    return wrap
