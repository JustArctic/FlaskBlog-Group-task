from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# Blueprint for all user-related routes (authentication, profiles, account management)
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # Redirect authenticated users away from the registration page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # Handle form submission
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) # Hash the user's password before storing it
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create new user instance
        # Save user to database
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # Redirect authenticated users away from login page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Look up user by email
        # Validate password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) # Log the user in, optionally remembering their session
            # Redirect to the page the user originally wanted to access
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Log the user out and redirect to home
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required # Only logged-in users can access their account page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # If a new profile picture was uploaded, save it
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data # Update username
        current_user.email = form.email.data # Update email
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account')) # Redirect to avoid form resubmission issues
    elif request.method == 'GET':
        # Pre-fill form fields with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) # Pagination for user-specific posts
    user = User.query.filter_by(username=username).first_or_404() # Fetch user or return 404
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: # Prevent logged-in users from requesting password resets
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Look up user by email
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form) # Render password reset request form


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # Prevent logged-in users from resetting passwords
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token) # Validate token and retrieve user
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) # Hash new password
        user.password = hashed_password # Update user's password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
