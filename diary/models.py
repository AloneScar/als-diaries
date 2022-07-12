from diary import db
from datetime import datetime


# 定义模
class Item(db.Model):
    title = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_last_commited = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'Item {self.title} => {self.date_last_commited}'
