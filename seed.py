"""sample data for blogly app users db"""

from app import app
from models import db, User

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(first_name="John", last_name='Smith', img_url='https://www.aspca.org/sites/default/files/cat-care_general-cat-care_body1-left.jpg')
    user2= User(first_name='Mary', last_name='Oak', img_url='https://www.akc.org/wp-content/uploads/2017/11/Golden-Retriever-Puppy.jpg')
    user3= User(first_name='Tyler', last_name='Doe')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()