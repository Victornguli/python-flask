from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class User(db.Model):
	""""Model representing users table"""

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(256), nullable = False, unique = True)
	password = db.Column(db.String(256), nullable = False)
	bucketlists = db.relationship(
		'BucketList', order_by = 'BucketList.id', cascade = 'all, delete-orphan'
	)

	def __init__(self, email, password):
		"""Initializes the user model with a password and email"""
		self.email = email
		self.password = Bcrypt().generate_password_hash(password).decode()

	def password_is_valid(self, password):
		"""Checks a submitted password against its stored hash"""
		return Bcrypt.check_password_hash(self.password, password)

	def save(self):
		"""Save a user to a database. This includes creating a new user and editing too"""
		db.session.add(self)
		db.session().commit()

	def generate_token(self, user_id):
		"""Generates JWT Token for user authorization"""
		try:
			payload = {
				'exp': datetime.utcnow() + timedelta(minutes = 5),
				'iat': datetime.utcnow(),
				'sub': user_id
			}

			jwt_string = jwt.encode(payload, current_app.config.get('SECRET'), algorithm = 'HS256')
			return jwt_string
		except Exception as ex:
			return str(ex)

	@staticmethod
	def decode_token(token):
		"""Decodes the access token for user Authorization"""
		try:
			payload = jwt.decode(token, current_app.config.get('SECRET'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return "Expired token. Login to get a new token"
		except jwt.InvalidTokenError:
			return "Invalid token. Register or Login to continue"

	def __repr__(self):
		return self.email


class BucketList(db.Model):
	"""Model representing bucket list table"""

	__tablename__ = 'bucketlists'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(255))
	date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
	date_modified = db.Column(
		db.DateTime, default = db.func.current_timestamp(),
		onupdate = db.func.current_timestamp())
	user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)

	def __init__(self, name):
		"""initialize with name."""
		self.name = name

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all():
		return BucketList.query.all()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return "<Bucketlist: {}>".format(self.name)
