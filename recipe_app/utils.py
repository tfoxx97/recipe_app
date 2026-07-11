from functools import wraps
from flask import request, render_template, flash, url_for, redirect
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
    
def get_current_user():
    '''Returns the public id of the currently logged in user, or None if no user is logged in. '''
    token = request.cookies.get('jwt_token')
    if not token:
        return None
    if token in blocklisted_tokens:
        return None
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return data['user']
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return None
    
def approval_required(func):
    '''User must be approved by admin in order to access endpoint'''
    @wraps(func)
    def decorated(*args, **kwargs):
        public_id = get_current_user()
        user = User.query.filter_by(public_id=public_id).first()
        if user and not user.is_approved:
            flash("Please wait until the admin has approved your access.", "warning")
            return redirect(url_for('recipes'))
        
        return func(*args, **kwargs)
    
    return decorated

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

def notify_admin_of_new_registration(new_user: User):
    ''' Method responsible for sending email notification to admin when a new user registers. 
    
    Parameters:
    -----------
    new_user: User
    
    Method uses Mail object from flask extension to send email to admin with information about the new user.
    '''
    admin = User.query.filter_by(is_admin=True).first()

    msg = Message('New User Registration',
                  sender='noreply@shreddit.com',
                  recipients=[admin.email])
    
    msg.body = f'''A new user {new_user.email} has registered and is awaiting approval. 
    Please review their information and approve or deny their registration.'''

    mail.send(msg)

def notify_user_of_approval(user: User):
    ''' Method responsible for sending email notification to user when their account is approved. 
    
    Parameters:
    -----------
    user: User
    
    Method uses Mail object from flask extension to send email to user notifying them of their account approval.
    '''
    msg = Message('Account Approved',
                  sender='noreply@shreddit.com',
                  recipients=[user.email])
    msg.body = f'''Your account has been approved by the admin. You can now login and start adding and updating recipes.'''

    mail.send(msg)