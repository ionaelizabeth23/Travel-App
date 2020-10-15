from flask import Blueprint
from flask import request, session, redirect, url_for
from flask import session
from flask import render_template
from .models import Destination

#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = Destination.query.all()
    return render_template('index.html', destinations=destinations)

# route to allow users to search
@mainbp.route('/search')
def search():
    if request.args['search']:
        dest = "%" + request.args['search'] + '%'
        destinations = Destination.query.filter(Destination.name.like(dest)).all()
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))
