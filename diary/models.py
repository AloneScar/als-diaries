from diary import db
import snowflake.client
from datetime import datetime


def get_snowflake_uuid():
    # Start-Process -WindowStyle hidden -FilePath "snowflake_start_server.exe" 
    return snowflake.client.get_guid()

# 定义模
class Item(db.Model):
    id = db.Column(db.String(), primary_key=True, default=get_snowflake_uuid())
    title = db.Column(db.String(), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_last_commited  = db.Column(db.DateTime(), default=datetime.utcnow)
    content_url = db.Column(db.String())


    def __repr__(self):
        return f'Item {self.title} => {self.date_last_commited}'