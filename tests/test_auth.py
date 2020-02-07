import unittest
import json
from app import create_app, db


class AuthTest(unittest.TestCase):
	"""Test class for authentication blueprint"""

	def setUp(self):
		"""Set up test environment and variables"""
		self.app = create_app("testing")
		self.client = self.app.test_client
		self.user_data = {
			'email': 'mail@example.com',
			'password': 'quirky_password'
		}

		with self.app.app_context():
			db.session.close()
			db.drop_all()
			db.create_all()

	def test_registration(self):
		"""Test user registration works correcty."""
		res = self.client().post('/auth/register', data = self.user_data)
		# get the results returned in json format
		result = json.loads(res.data.decode())
		# assert that the request contains a success message and a 201 status code
		self.assertEqual(result['message'], "You registered successfully. Please log in.")
		self.assertEqual(res.status_code, 201)

	def test_already_registered_user(self):
		"""Test that a user cannot be registered twice."""
		res = self.client().post('/auth/register', data = self.user_data)
		self.assertEqual(res.status_code, 201)
		second_res = self.client().post('/auth/register', data = self.user_data)
		self.assertEqual(second_res.status_code, 202)
		# get the results returned in json format
		result = json.loads(second_res.data.decode())
		self.assertEqual(
			result['message'], "User already exists. Please login.")

	def test_user_login(self):
		"""Test registered user can login."""
		res = self.client().post('/auth/register', data = self.user_data)
		self.assertEqual(res.status_code, 201)
		login_res = self.client().post('/auth/login', data = self.user_data)
		# get the results in json format
		result = json.loads(login_res.data.decode())
		# Test that the response contains success message
		self.assertEqual(result['message'], "You logged in successfully.")
		# Assert that the status code is equal to 200
		self.assertEqual(login_res.status_code, 200)
		self.assertTrue(result['access_token'])

	# def test_non_registered_user_login(self):
	# 	"""Test non registered users cannot login."""
	# 	# define a dictionary to represent an unregistered user
	# 	not_a_user = {
	# 		'email': 'not_a_user@example.com',
	# 		'password': 'nope'
	# 	}
	# 	# send a POST request to /auth/login with the data above
	# 	res = self.client().post('/auth/login', data = not_a_user)
	# 	# get the result in json
	# 	result = json.loads(res.data.decode())
	#
	# 	# assert that this response must contain an error message
	# 	# and an error status code 401(Unauthorized)
	# 	self.assertEqual(res.status_code, 401)
	# 	self.assertEqual(
	# 		result['message'], "Invalid email or password, Please try again")


if __name__ == "__main__":
	unittest.main()
