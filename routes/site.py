from flask import Blueprint, render_template, request, redirect

from datetime import date
from services import pirmas
from models import Event
from database import db


bp = Blueprint('site', __name__)

@bp.route('/')
@bp.route('/home')
def index():
    """atvaizduoja pradžios puslapį"""
    return render_template('index.html', title='"Kardo ir žagrės" sąjunga')


@bp.route('/about')
def about():
    """atvaizduoja apie mus puslapį"""
    apie = pirmas.add_aboutus_text_from_file()
    return render_template('about.html', title='Apie mus', apie=apie)


@bp.route('/posts')
def posts():
    """atvaizduoja įrašus apie įvykius"""
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template('posts.html', title='Pranešimai', events=events)


@bp.route('/post/<int:id>')
def post_view(id):
    """atvaizduoja pasirinktą įrašą su konkrečiu id"""
    event = Event.query.get(id)
    return render_template('post_view.html', title='Pranešimas', event=event)


@bp.route('/post/<int:id>/delete')
def post_delete(id):
    """pašalina iš bazės pasirinktą įrašą su konkrečiu id"""
    event = Event.query.get_or_404(id)
    try:
        db.session.delete(event)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Įvyko klaida trinant įrašą iš "Kardo ir žagrės" sąjungos!'


@bp.route('/post/create', methods=['POST', 'GET'])
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


@bp.route('/post/<int:id>/modify', methods=['POST', 'GET'])
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
    