from app import app, db
from forms import  RegisterForm, LoginForm
from models import User
from flask.ext.login import login_user, logout_user, login_required
from flask import render_template, redirect, request, url_for, flash

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register',methods = ['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email = form.email.data, nickname = form.nickname.data, password = form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now log in')
		return redirect(url_for('login'))
	return render_template('register.html', form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('index'))
		flash('Invalid email or password')
	return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('index'))