from hashlib import new
from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import EditFeedbackForm, RegisterForm, LoginForm, NewFeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flaskfeedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "feedback.gov"

connect_db(app)

@app.route('/')
def redirect_to_register():
    """right now redirects to register page"""
    if "username" not in session:
        return redirect('/register')
    else:
        username = session['username']
        return redirect(f'/users/{username}')
    
## USER ROUTES ##

@app.route('/register', methods=["GET","POST"])
def show_registration_form():
    """shows the registration form"""
    form = RegisterForm()
    if form.validate_on_submit():
        u = form.username.data
        username = u.lower()
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username has already been taken.')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        return redirect(f'/users/{username}')
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def show_login_form():
    """shows the login form"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        if User.authenticate(username, password):
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            flash("Invalid username or password.")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user_profile(username):
    """shows the page for a user"""
    if "username" not in session:
        flash("You need to be logged in to view that page.")
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template('profile.html', user=user, feedback=feedback)
        
@app.route('/users/<username>/delete', methods = ["POST"])
def delete_user(username):
    """deletes the user (only if that user is the one who's signed in)"""
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        log_out()
    else:
        flash('You must be logged in as that user to delete them.')
        return redirect(f'/users/{username}')

@app.route('/logout')
def log_out():
    """logs out the user"""
    session.clear()
    return redirect('/')

## FEEDBACK ROUTES ##

@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username): 
    """add feedback"""
    if session['username'] == username:
        form = NewFeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        return render_template('new_feedback.html', form=form)
    else:
        flash('You must be logged in as that user to make a feedback post for them.')
        return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedbackid>/edit', methods=['GET', "POST"])
def edit_feedback(feedbackid):
    """edit feedback"""
    feedback = Feedback.query.get_or_404(feedbackid)
    username = feedback.username
    if session['username'] == username:
        form = EditFeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{username}')
        return render_template('edit_feedback.html', form=form)

    else:
        flash("You can't edit another user's feedback.")
        return redirect(f'/users/{feedback.username}')

@app.route('/feedback/<int:feedbackid>/delete', methods=['POST'])
def delete_feedback(feedbackid):
    """deletes feedback"""
    feedback = Feedback.query.get_or_404(feedbackid)
    username = feedback.username
    if session['username'] == username:
        db.session.delete(feedback)
        db.session.commit()
    else:
        flash("You can't delete another user's feedback.")
    return redirect(f'/users/{username}')