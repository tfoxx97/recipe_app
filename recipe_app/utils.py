from functools import wraps
from flask import request, render_template, flash, url_for
from flask_mail import Message
import jwt
from datetime import datetime, timedelta, timezone
from recipe_app import app, mail
from recipe_app.models import User, Recipe

non_capitalized_words = ['and', 'a', 'with', 'the', 'as', 'but', 'by', 'for', 'in', 'nor', 'of', 'on', 'up']
blocklisted_tokens = set()

def capitalize_title(name: str):
    name = name.split(" ")
    cap_title = [n.capitalize() if n not in non_capitalized_words else n for n in name]
    return " ".join(cap_title)

def is_logged_in():
    token = request.cookies.get('jwt_token')
    if not token:
        return False
    
    if token in blocklisted_tokens:
        return False
    
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return True
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return False

def token_required(func):
    '''JSON web token required in order to view this page'''
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token or token in blocklisted_tokens:
            flash("Missing token. Please login", "warning")
            return render_template("login.html")
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            flash("Invalid or expired token. Please login", "warning")
            return render_template("login.html")
        
        return func(*args, **kwargs)
    
    return decorated

def logout_early(token):
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.filter_by(public_id=data['user']).first()
    if user:
        blocklisted_tokens.add(token)

def create_recipe_dicts():
    breakfast = {}
    lunch = {}
    dinner = {}

    breakfast_items = Recipe.query.filter_by(category='breakfast').all()
    lunch_items = Recipe.query.filter_by(category='lunch').all()
    dinner_items = Recipe.query.filter_by(category='dinner').all()

    for b in breakfast_items:
        name = capitalize_title(b.name)
        breakfast[name] = b.id

    for l in lunch_items:
        name = capitalize_title(l.name)
        lunch[name] = l.id

    for d in dinner_items:
        name = capitalize_title(d.name)
        dinner[name] = d.id

    return breakfast, lunch, dinner

def get_reset_token(user: User):
    token = jwt.encode(
        {'user': user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        app.config['SECRET_KEY'], 
        algorithm='HS256')
    return token

def send_reset_email(user: User):
    ''' Method responsible for sending reset password email. 
    
    Parameters: 
    -----------
    user: User
    
    Method uses Mail object from flask extension to send reset password email to the 
    proper recipient with a given serialized token.
    '''
    token = get_reset_token(user)
    msg = Message('Password Reset Request', 
                  sender='noreply@shreddit.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit: {url_for('reset_token', token=token, _external=True)} 

If you did not make this request, kindly disregard this email.

Thank you,

-Tyler
'''
    mail.send(msg)