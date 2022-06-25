import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f)
        if session.get("user_id") is None:
            return redirect("/login?"+f.__name__)
        return f(*args, **kwargs)
    return decorated_function