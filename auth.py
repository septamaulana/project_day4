from flask import request, Response, session, url_for, redirect, flash
from functools import wraps
from models import User

def login_required(f):
    @wraps(f)
    def wraper(*args, **kwargs):
        session_user = session.get('username')
        if session_user is not None:
            check_user = User.query.filter_by(username=session_user).first_or_404()
            if check_user:
                return f(*args, **kwargs, user=check_user)
            else:
                session.pop('username')
        else:
            flash('You must login first!')
            return redirect(url_for('login'))
    return wraper