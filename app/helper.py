from app.db import db
from app.models import User

db.create_all()
user1 = User(username='user1', email='test@email.com')
user2 = User(username='user2', email='test2@email.com')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

print(User.query.all())