from project import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    age = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'address': self.address,
            'phone': self.phone,
            'age': self.age,
            'active': self.active
        }

    def __init__(self, username, email, address, phone, age):
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.age = age
