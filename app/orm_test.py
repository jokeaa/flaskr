from app import db,models
u = models.User(nickname='john',email='123123')
db.session.add(u)
db.session.commit()