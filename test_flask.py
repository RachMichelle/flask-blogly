from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


with app.app_context():
    db.drop_all()
    db.create_all()
    
class UserTestCase(TestCase):
    """test view functions"""

    def setUp(self):
        """add test user"""
        with app.app_context():

            user=User(first_name='test', last_name='test')
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """clean up"""
        with app.app_context():
            db.session.rollback()

    def test_home_redirect(self):
        """test home route results in redirection"""
        with app.test_client() as client:
            resp=client.get('/')

            self.assertEqual(resp.status_code, 302)

    def test_user_list(self):
        """test /users off of / redirect"""
        with app.test_client() as client:
            resp=client.get('/', follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('<button>Add a New User</button>', html)

    def test_create_user_form(self):
        """test create user form page"""
        with app.test_client() as client:
            resp=client.get('/users/new')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)
            self.assertIn('<button>Submit</button>', html)

    def test_create_user(self):
        """test create user post"""

        with app.test_client() as client:
            data = {"first_name":"test2", "last_name":"test2", "img_url":"test"}
            resp = client.post('users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    