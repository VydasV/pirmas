from datetime import date, timedelta
from database import db
from models import Event



def delete_old_posts():
    yesterday = date.today() - timedelta(days=1)
    Event.query.filter(Event.event_date<=yesterday).delete()
    db.session.commit()
    return
