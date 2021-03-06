from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(64), unique = True)
	password_hash = db.Column(db.String(128))
	lists = db.relationship('Item', backref = 'user')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '== User %r==' % (self.nickname)

class Item(db.Model):
	__tablename__ = 'lists'
        id = db.Column(db.Integer, primary_key = True)
        title = db.Column(db.String(32))
        detail = db.Column(db.String(128))
        tag = db.Column(db.String(32))
	timestamp = db.Column(db.DateTime)
	before = db.Column(db.String(64))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



