import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import date
from services import pirmas


def create_app():
    """sukuria puslapį naudojant Flask"""
    app = Flask(__name__)

    # konfiguracija iš config.py failo
    app.config.from_object(os.getenv('FLASK_CONFIG', 'config.DevConfig'))
    db = SQLAlchemy(app)


    class Event(db.Model):
        # apibrėžiam duombazės stulpelius
        id = db.Column(db.Integer, primary_key=True)
        event_text = db.Column(db.String(256), nullable=False)
        event_date = db.Column(db.Date)

        def __repr__(self):
            return '<Event %r>' % self.id


    @app.route('/')
    @app.route('/home')
    def index():
        """atvaizduoja pradžios puslapį"""
        return render_template('index.html', title='"Kardo ir žagrės" sąjunga')


    @app.route('/about')
    def about():
        """atvaizduoja apie mus puslapį"""
        apie = pirmas.add_aboutus_text_from_file()
        return render_template('about.html', title='Apie mus', apie=apie)


    @app.route('/posts')
    def posts():
        """atvaizduoja įrašus apie įvykius"""
        events = Event.query.order_by(Event.id.desc()).all()
        return render_template('posts.html', title='Pranešimai', events=events)


    @app.route('/post/<int:id>')
    def post_view(id):
        """atvaizduoja pasirinktą įrašą su konkrečiu id"""
        event = Event.query.get(id)
        return render_template('post_view.html', title='Pranešimas', event=event)


    @app.route('/post/<int:id>/delete')
    def post_delete(id):
        """pašalina iš bazės pasirinktą įrašą su konkrečiu id"""
        event = Event.query.get_or_404(id)

        try:
            db.session.delete(event)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Įvyko klaida trinant įrašą iš "Kardo ir žagrės" sąjungos!'


    @app.route('/post/create', methods=['POST', 'GET'])
    def create_event():
        """sukuria naują duomenų bazės įrašą"""
        if request.method == "POST":
            if request.form['date'] == '':
                # jei neįvesta data, data=šiandien
                event_date = date.today()
            else:
                # date grąžina str, todėl reikia konvertuoti į datos tipą
                event_date = date.fromisoformat(request.form['date'])
            event_text = request.form['text']

            record = Event(event_text=event_text, event_date=event_date)

            try:
                db.session.add(record)
                db.session.commit()
                return redirect('/posts')
            except:
                return 'Įvyko klaida įrašant pranešimą apie "Kardo ir žagrės" sąjungą!'
        else:
            return render_template('post_create.html', title='Naujas pranešimas')


    @app.route('/post/<int:id>/modify', methods=['POST', 'GET'])
    def modify_event(id):
        """Koreguoja pagal id iš bazės pasirinktą įrašą"""
        event = Event.query.get(id)
        if request.method == "POST":
            # date grąžina str, todėl reikia konvertuoti į datos tipą
            event.event_date = date.fromisoformat(request.form['date'])
            event.event_text = request.form['text']

            try:
                db.session.commit()
                return redirect('/posts')
            except:
                return 'Įvyko klaida redaguojant pranešimą apie "Kardo ir žagrės" sąjungą!'
        else:
            return render_template('post_modify.html', title='Redaguoti įvykį', event=event)
        
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
