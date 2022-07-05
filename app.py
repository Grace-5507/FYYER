

from ctypes import addressof
from hashlib import new
from itertools import count
import json
from unicodedata import name
from unittest import result
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from markupsafe import Markup
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *


from models import db, Venue, Artist, Show
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate=Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lornaolum:1234@localhost:5432/fyyur'




class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Columnn(db.String(120))
    seeking_talent = db.Column(db.boolean, default=False)
    seeking_description = db.Column(db.string(120))
    upcoming_shows = db.Column(db.string(120))
    upcoming_shows_count =db.Column(db.integer)
    
    
    def __repr__(self):
        return f'<Venue {self.name} {self.image_link}>'
    
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Columnn(db.String(120))
    seeking_talent = db.Column(db.boolean, default=False)
    seeking_description = db.Column(db.string(120))
    upcoming_shows = db.Column(db.string(120))
    upcoming_shows_count =db.Column(db.integer)
    
    
    def __repr__(self):
        return f'<Artist {self.name} {self.image_link}>'
      
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.integer)
    venue_name = db.Column(db.String(120))
    artist_id = db.Column(db.integer)
    artist_name = db.Column(db.String(120))
    artist_image_link = db.Column(db.String(120))
    start_time = db.Column(db.datetime)


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime



@app.route('/')
def index():
  return render_template('pages/home.html')



@app.route('/venues')
def venues():
    data = Venue.query.all()
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
    print( list(data))
    return render_template('pages/show_venue.html', venue=Venue.query.all())

app.route('/venues/search', methods=['POST'])
def search_venues():
  body={}
  venue_search = request.form['search_term']
  search = '%{}%'.format(venue_search)
  results = Venue.session.query.filter_by(name).all()
  return render_template('pages/search_venues.html', results=results)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
   try:
    new_Venue=VenueForm(new_name=request.form('name'),
                        new_city=request.form('city'),
                        new_state=request.form('state'),
                        new_address=request.form('adress'),
                        new_phone=request.form('phone'), 
                        new_image_link=request.form('image_link'),
                        new_facebook_link=request.form('facebook_link'),
                        new_seeking_talent=request.form('seeking_talent'), 
                        new_talent_description=request.form('talent_description'),
                        new_upcoming_shows=request.form('upcoming_shows'), 
                        new_upcominng_show_count=request.form('upcoming_show_count'))
    db.session.add(new_Venue)
    db.session.commit()
    
   except:
      db.session.rollback()
      flash('An error occurred. Venue ' + name + ' could not be listed.')
            
   finally:
        db.session.close()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    
    try:
       Venue.query.filter_by(id=venue_id).delete()
       db.session.commit()
       
    except Exception as e:
        print('error')
  
    finally:
         db.session.close()
       
         return { 'success': True }

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.filter_by(id) and Artist.query.filter_by(name)
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    Artist_search=request.form('search_term', '')
    body={}
    search = '%{}%'.format(Artist_search)
    results = Artist.session.query.filter_by(name).all()
    return render_template('pages/search_venues.html', results=results)

  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
   
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data=Artist.query.filter_by(artist_id)
 
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
    data = list(filter(lambda d: d['id'] == artist_id))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    req=request.form()
    artist=Artist.query.filter_by(id=artist_id)
    artist.artist_id =req('artist_id')
  
  # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
   try: 
    req = request.form(artist_id)  
    new_artist_id = request.form('artist_id')
    db.session.add(new_artist_id)
    db.session.commit()
    
   except:
         db.session.rollback()
   finally:
          db.session.close() 
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

          return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    request.form.get()
    venue =Venue.session.query.filter_by(venue_id)
    
    
  
  # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:   
        venue = request.form.get()
        new_venue_id = request.form('venue_id')
        db.session.add(new_venue_id)
        db.session.commit()
    except:
           db.session.rollback()
    finally:
           db.session.close()
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
   try:
     new_artist =ArtistForm(new_name=request.form('name'),
                        new_city=request.form('city'),
                        new_state=request.form('state'),
                        new_genres=request.form('genres'),
                        new_image_link=request.form('image_link'),
                        new_facebook_link=request.form('facebook_link'),
                        new_seeking_talent=request.form('seeking_talent'), 
                        new_seeking_description=request.form('talent_description'),
                        new_upcoming_shows=request.form('upcoming_shows'), 
                        new_upcominng_show_count=request.form('upcoming_show_count'))
     db.session.add(new_artist)
     db.session.commit()
   except:
           db.session.rollback()
           flash('An error occurred.Artist ' + name + ' could not be listed.' )
            
   finally:
        db.session.close()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
  
@app.route('/shows')
def shows():
  data=Show.session.query.all()
  artist_id=Artist.session.get(artist_id)
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  past_shows = []
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now().all())
  upcoming_shows = []
  return render_template('pages/shows.html', data=Show.session.query.all())
  
  
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
   

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
        
        new_show = ShowForm(new_venue_id=request.form('venue_id'), 
                            new_venue_name=request.form('venue_name'),
                            new_artist_id=request.form('artist_id'),
                            new_artist_image_link=request.form('artist_image_link'))
        
        db.session.add(new_show)
        db.session.commit()
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
flash('An error occurred. Show could not be listed.')
    
                                                            
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
