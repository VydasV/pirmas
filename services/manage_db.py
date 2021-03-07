from datetime import date, timedelta
from database import db


def delete_old_posts_from_db(posts):
    """pašalina iš duomenų bazės senesnius nei šiandien įrašus"""
    yesterday = date.today() - timedelta(days=1)
    try:
        posts_query = posts.query.filter(posts.event_date <= yesterday)
        records = len(posts_query.all())
        posts_query.delete()
        db.session.commit()
        return f'Seni įrašai pašalinti ({records})'
    except:
        return 'Įvyko klaida trinant įrašus iš "Kardo ir žagrės" sąjungos!'
