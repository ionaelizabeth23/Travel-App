from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from .models import Destination,Comment,User
from .forms import CommentForm, DestinationForm
from . import db
from flask import session
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user


#create a blueprint
bp = Blueprint('destination', __name__, url_prefix='/destinations')

#create a page that will show the details fo the destination
@bp.route('/<id>') 
def show(id): 
  destination = Destination.query.filter_by(id=id).first()  
  cform = CommentForm()
  return render_template('destinations/show.html', destination=destination, form=cform)


@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  form = DestinationForm()
  if form.validate_on_submit():
    # if the form was successfully submitted
    # access the values in the form data
    destination = Destination(name=form.name.data, 
                description=form.description.data,
                image=form.image.data,
                currency=form.currency.data)
    # add the object to the db session
    db.session.add(destination)
    # commit to the database
    db.session.commit()

    #flash('Successfully created new travel destination', 'success')
    print('Successfully created new travel destination', 'success')
    return redirect(url_for('destination.create'))

  return render_template('destinations/create.html', form=form)

@bp.route('/<destination>/comment', methods = ['GET', 'POST']) 
@login_required 
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Destination.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj, user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=destination))


#############   USE THIS CODE LATER ######################
def get_destination():
    #creating the description of Brazil
    b_desc= """Brazil is considered an advanced emerging economy.
    It has the ninth largest GDP in the world by nominal, and eight by PPP measures. 
    It is one of the world\'s major breadbaskets, being the largest producer of coffee for the last 150 years."""
    # an image location
    image_loc='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFyC8pBJI2AAHLpAVih41_yWx2xxLleTtdshAdk1HOZQd9ZM8-Ag'
    destination = Destination('Brazil',b_desc,image_loc,'10 R$')
    # a comment
    comment = Comment("User1", "Visited during the olympics, was great",'2019-11-12 11:00:00')
    destination.set_comments(comment)
    comment2 = Comment("User B", "Cool stuff",'2019-11-12 11:00:01')
    destination.set_comments(comment2)
    return destination
