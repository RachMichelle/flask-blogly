"""sample data for blogly app users db"""

from app import app
from models import db, User, Post

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(first_name="John", last_name='Smith', img_url='https://www.aspca.org/sites/default/files/cat-care_general-cat-care_body1-left.jpg')
    user2= User(first_name='Mary', last_name='Oak', img_url='https://www.akc.org/wp-content/uploads/2017/11/Golden-Retriever-Puppy.jpg')
    user3= User(first_name='Tyler', last_name='Doe')

    db.session.add_all([user1, user2, user3])

    db.session.commit()

    p1= Post(title='test', content='test post 1', user_id=1)
    p2= Post(title='test 2', content='test post 2', user_id=1)
    p3= Post(title='test 3', content='test post 3', user_id=2)
    p4= Post(title='test 4', content='test post 4', user_id=3)

    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
