from app import app, db, file_upload
from forms import  RegisterForm, LoginForm, ItemForm, UploadForm
from models import User,Item
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, request, url_for, flash, send_from_directory
import datetime, os

@app.route('/index')
def index():
	if current_user.is_authenticated:
		user = User.query.filter_by( id = current_user.id).first()
		lists = user.lists
		return render_template('index.html', lists = lists)
	else:
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


@app.route('/publish', methods = ['GET','POST'])
@login_required
def publish():
	form = ItemForm()
	if form.validate_on_submit():
		item = Item(title = form.title.data, detail = form.detail.data, tag = form.tag.data, before = form.before.data, timestamp = datetime.datetime.now(), user_id = current_user.id)
 		db.session.add(item)
		db.session.commit()
		return redirect((url_for('index')))
	return render_template('publish.html', form = form)


@app.route('/upload', methods = ['GET','POST'])
@login_required
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		file_name = file_upload.save(form.file.data, folder = str(current_user.id))
		file_url = file_upload.url(file_name)
		return redirect(url_for('my_files'))

	else:
		file_url = None

	return render_template('upload.html', form = form, file_url = file_url)

@app.route('/download/<user_id>/<file_name>', methods = ['GET', 'POST'])
@login_required
def  download(user_id,file_name):
	return send_from_directory(app.config['UPLOADED_DEFAULT_DEST'] + user_id, file_name, as_attachment=True)

@app.route('/delete/<file_name>', methods = ['GET', 'POST'])
@login_required
def  delete(file_name):
	return delete_file(app.config['UPLOADED_DEFAULT_DEST'] + str(current_user.id) + '/' + file_name)

@app.route('/files', methods = ['GET','POST'])
@login_required
def my_files():
	my_list = os.listdir(app.config['UPLOADED_DEFAULT_DEST'] + str(current_user.id))
	all_path = os.listdir(app.config['UPLOADED_DEFAULT_DEST'])
	all_dict = dict()
	for  path in all_path:
		if os.path.isdir(path):
			pass
		else:
			all_dict[path] = os.listdir(app.config['UPLOADED_DEFAULT_DEST'] + path)

	return render_template('files.html', my_list = my_list, all_dict = all_dict)
	
def delete_file(file_name):
	os.remove(file_name)
	return redirect(url_for('my_files'))


