from flask_demo_site import mysql, app
from datetime import datetime

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(32), nullable=False)
#     image = db.Column(db.String(20), nullable=False, default='default.jpg')
#     date_created = db.Column(db.DateTime, default=datetime.utcnow )
    
#     def __repr__(self):
#         return f'{self.username} : {self.email} : {self.password} : {self.date_created}'
    
# with app.app_context():
#     db.create_all()