from flask import *
from app.db import *
from app.routes.requires_auth import *

meet = Blueprint('meet', __name__, template_folder='templates')

@meet.route('/meets', methods=['GET'])
@requires_auth
def meets():
    return render_template("meets.html", meets = Meet.all())

@meet.route('/meets', methods=['POST'])
@requires_auth
def add_meet():
    Meet(name = request.form["name"]).save()
    return redirect("/meets")
