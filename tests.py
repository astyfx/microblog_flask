#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_avatar(self):
		u = User(nickname = 'astyfx', email = 'astyfx@gmail.com')
		avatar = u.avatar(128)
		expected = 'http://www.gravatar.com/avatar/7c19b76d0470e8b8fc9e130e3fbba0e8'
		assert avatar[0:len(expected)] == expected

	def test_make_unique_nickname(self):
		u = User(nickname = 'astyfx', email = 'astyfx@gmail.com')
		db.session.add(u)
		db.session.commit()
		nickname = User.make_unique_nickname('astyfx')
		assert nickname != 'astyfx'
		u = User(nickname = nickname, email = 'susan@gmail.com')
		db.session.add(u)
		db.session.commit()
		nickname2 = User.make_unique_nickname('astyfx')
		assert nickname2 != 'astyfx'
		assert nickname2 != nickname

if __name__ == '__main__':
	unittest.main()