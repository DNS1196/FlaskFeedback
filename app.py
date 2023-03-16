from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm,  FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flaskfeedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secretSauce123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



with app.app_context():
    connect_db(app)
    db.create_all()
    

@app.route('/')
def home_page():
    """Homepage of site; redirect to register."""
     
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register a user: produce form and handle form submission."""
    
    # if "username" in session:
    #     return redirect(f"/users/{session['username']}")
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        
        return redirect(f"/user/{new_user.username}")
    else:
        return render_template('register.html', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    # if "username" in session:
    #     return redirect("/secret")
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username,password)
        
        if user:
            session['username'] = user.username
            return redirect(f"/user/{user.username}")
        
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")


@app.route('/user/<username>')
def show_user(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get_or_404(username)
    form = DeleteForm()
    
    return render_template('show_user.html', user=user, form=form)



@app.route('/user/<username>/delete', methods=["POST"])
def delete_user(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    
    return redirect('/login')

@app.route('/user/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        new_feedback= Feedback(title=title, content=content, username=username)
        
        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f'/user/{username}')
         
    else:
        return render_template('feedback.html', form=form)
    
    
@app.route('/feedback/<int:feedback_id>/update', methods= ["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        return redirect(f'/user/{feedback.username}')
                
    else:
        return render_template('update_feedback.html', form=form, feedback=feedback)



@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    
    return redirect (f'/user/{feedback.username}')