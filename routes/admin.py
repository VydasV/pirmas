from flask import Blueprint, make_response

from models import Event
from services.manage_db import delete_old_posts_from_db

bp = Blueprint('admin', __name__)


@bp.route('/delete')
def delete_old_posts():
    text = delete_old_posts_from_db(Event)
    return make_response(text)
    