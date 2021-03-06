from database import db


class Event(db.Model):
        # apibrėžiam duombazės stulpelius
        id = db.Column(db.Integer, primary_key=True)
        event_text = db.Column(db.String(256), nullable=False)
        event_date = db.Column(db.Date)

        def __repr__(self):
            return '<Event %r>' % self.id
    