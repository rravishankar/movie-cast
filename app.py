import os, json, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Artist, Movie, MovieCast
import logging
from logging import Formatter, FileHandler
from auth.auth import AuthError, requires_auth


logger = None
ARTISTS_PER_PAGE = 5
MOVIES_PER_PAGE = 5
MOVIECAST_PER_PAGE = 5

def paginate_artists(request, artists):
  page = request.args.get('page',1, type=int)
  start = (page-1) * ARTISTS_PER_PAGE
  end = start + ARTISTS_PER_PAGE
  #TBD will need something different for large datasets - when there are millios of rows
  # https://stackoverflow.com/questions/7389759/memory-efficient-built-in-sqlalchemy-iterator-generator
  req_artists = artists[start:end]
  artists_json = {artist.id: {"name": artist.name, "age": artist.age, "gender": artist.gender} for artist in req_artists}
  return artists_json


def paginate_movies(request, movies):
  page = request.args.get('page',1, type=int)
  start = (page-1) * MOVIES_PER_PAGE
  end = start + MOVIES_PER_PAGE
  #TBD will need something different for large datasets - when there are millios of rows
  # https://stackoverflow.com/questions/7389759/memory-efficient-built-in-sqlalchemy-iterator-generator
  req_movies = movies[start:end]
  movie_json = {movie.id: {"title": movie.title, "release_date": movie.release_date.strftime("%A %d. %B %Y")} for movie in req_movies}
  return movie_json



def create_app(test_config=None):
  # create and configure the apapp = Flask(__name__)
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  # moment = Moment(app)
  # migrate = Migrate(app, db)
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response
  
  @app.route('/actors')
  @requires_auth("get:actors")
  def get_artists(payload):
    artists = Artist.query.order_by(Artist.name).all()
    logger.debug("Got artists type {}".format(type(artists)))
    artist_json = paginate_artists(request, artists)

    if len(artist_json) == 0:
      abort(404)

    app.logger.debug("Got artist_json:{}".format(artist_json))

    return jsonify({
      'success': True,
      'actors': artist_json
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_artist(payload):
    req_data_dict = json.loads(request.data)
    app.logger.debug("Got request", req_data_dict)
    if "name" not in req_data_dict or "age" not in req_data_dict or "gender" not in req_data_dict:
      abort(400)
    name = req_data_dict["name"]
    age = req_data_dict["age"]
    gender = req_data_dict["gender"]
    artist = Artist(name= name, age = age, gender = gender)
    artist.insert()
    artist_single = [artist.long()]
    return jsonify({
            'success': True,
            'actors': artist_single
    })

  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def del_artist(id):
    app.logger.debug("Got to delete artist {}".format(id))
    errno = 0
    
    try:
      MovieCast.query.filter_by(artist_id=id).delete()
      app.logger.debug("Deleted artist id {} from MovieCast table".format(id))      
      artist = Artist.query.get(id)
      if artist == None:
        app.logger.debug("No artist found with id {}".format(id))
        errno = 404
        abort(errno)
      artist.delete()
      app.logger.debug("Artist with id {} deleted".format(id))
      return jsonify({
        'success': True
      })
    except Exception as e:
      app.logger.error("delete_artist:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno)

  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('update:actors')
  def update_artist(id):
    app.logger.debug("Artist id {}".format(id))
    errno = 0
    
    try:
      artist = Artist.query.get(id)
      if artist == None:
        app.logger.error("No artist found with id {}".format(id))
        errno = 404
        abort(errno)
      logger.debug("Got artist {}".format(artist))
      body_json = request.get_json()
      artist.name = body_json.get('name', artist.name)
      artist.age = body_json.get('age', artist.age)
      artist.gender = body_json.get('gender', artist.gender)

      artist.update()
      app.logger.debug("artist with id {} updated".format(id))
      return jsonify({
        'success': True
      })
    except Exception as e:
      app.logger.error("delete_movie:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno)


  @app.route('/movies')
  @requires_auth("get:movies")
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.title).all()
    app.logger.debug("Got movies type:{}".format(type(movies)))
    # movie_json = {movie.id: {"title": movie.title, "release_date": movie.release_date.strftime("%A %d. %B %Y")} for movie in movies}
    movie_json = paginate_movies(request, movies)
    app.logger.debug("Got movie_json:{}".format(movie_json))
    if len(movie_json) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': movie_json
    })

  # @app.route('/movies', methods=['POST'])
  # @requires_auth("post:movies")
  # def add_movie(payload):
  #   body_json = request.get_json()
  #   app.logger.debug("Got request", body_json)
  #   errno = 0
    
  #   try:
  #     if request.is_json:
  #       print("is json")
  #       data = request.get_json()
  #       logger.debug("type of data {}".format(type(data))) # type dict
  #       logger.debug("data as string {}".format(json.dumps(data)))
  #       logger.debug ("keys {}".format(json.dumps(data.keys())))
  #     return jsonify(message='success')
  #     # if "title" not in req_data_dict or "release_date" not in req_data_dict:
  #     #   errno = 400
  #     #   abort(errno)
  #     # title = req_data_dict["title"]
  #     # release_date = req_data_dict["release_date"]
  #     # movie = Movie(title=title, release_date=release_date)
  #     # movie.insert()
  #     # movie_single = [movie.long()]
  #     # return jsonify({
  #     #         'success': True,
  #     #         'movies': movie_single
  #     # })
  #   except Exception as e:
  #     app.logger.error("insert_movie:Got exception {}".format(e))
  #     if errno == 0:
  #       abort(422)
  #     else:
  #       abort(errno) 

#Older method works without payload in add_movie parameter and without requires_auth
  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movies")
  def add_movie(payload):
    req_data_dict = json.loads(request.data)
    app.logger.debug("Got request {}".format(req_data_dict))
    errno = 0
    
    try:
      if "title" not in req_data_dict or "release_date" not in req_data_dict:
        errno = 400
        abort(errno)
      title = req_data_dict["title"]
      release_date = req_data_dict["release_date"]
      movie = Movie(title=title, release_date=release_date)
      movie.insert()
      movie_single = [movie.long()]
      return jsonify({
              'success': True,
              'movies': movie_single
      })
    except Exception as e:
      app.logger.error("insert_movie:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno) 


  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def del_movie(id):
    app.logger.debug("Got to delete movie {}".format(id))
    errno = 0
    
    try:
      nrows_del = MovieCast.query.filter_by(movie_id=id).delete()
      app.logger.debug("Deleted {} entries for movie id {} from MovieCast table".format(nrows_del, id))      
      movie = Movie.query.get(id)
      if movie == None:
        app.logger.debug("No movie found with id {}".format(id))
        errno = 404
        abort(errno)
      movie.delete()
      app.logger.debug("movie with id {} deleted".format(id))
      return jsonify({
        'success': True
      })
    except Exception as e:
      app.logger.error("delete_movie:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno)

  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('update:movies')
  def update_movie(id):
    app.logger.debug("Movie id {}".format(id))
    errno = 0
    
    try:
      movie = Movie.query.get(id)
      if movie == None:
        app.logger.debug("No movie found with id {}".format(id))
        errno = 404
        abort(errno)
      body_json = request.get_json()
      movie.title = body_json.get('title', movie.title)
      movie.release_date = body_json.get('release_date', movie.release_date)
      movie.update()
      app.logger.debug("movie with id {} updated".format(id))
      return jsonify({
        'success': True
      })
    except Exception as e:
      app.logger.error("delete_movie:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno)


  @app.route('/moviecast')
  def get_moviecast():
    mc_list_full = MovieCast.query.order_by(MovieCast.movie_id).all()
    app.logger.debug("Got mc list:{}".format(mc_list_full))

    page = request.args.get('page',1, type=int)
    start = (page-1) * MOVIECAST_PER_PAGE
    end = start + MOVIECAST_PER_PAGE
    moviecast = mc_list_full[start:end]

    if len(moviecast) == 0:
      abort(404)



    movie_num = 0
    artistid_list = []
    movie_and_cast = []
    movie_details = {}
    for mc in moviecast:
      app.logger.debug("Got mc:{}".format(mc))
      if movie_num != mc.movie_id:
        # Get movie title
        mov = Movie.query.get(mc.movie_id)
        movie_num = mc.movie_id
        movie_details = {}
        artistid_list = []
        # movie_name = "Movie_Name" + str(mc.movie_id)
        movie_title = mov.title
        movie_rel_date = mov.release_date
        app.logger.debug("Date type is {}".format(type(movie_rel_date)))
        movie_and_cast.append(movie_details)
        # movie_details["mc_id"] = mc.id
        # movie_details["movie_id"] = mc.movie_id
        movie_details["Title"] = movie_title
        movie_details["Release Date"] = movie_rel_date.strftime("%A %d. %B %Y")
      
      # artist_name = "Artist_Name" + str(mc.artist_id)
      artist = Artist.query.get(mc.artist_id)
      artist_name = artist.name
      artistid_list.append(artist.id)
      if "Actors" in movie_details.keys():
        # Get actor name
        movie_details["Actors"] = movie_details["Actors"] + ", " + artist_name
      else:
        movie_details["Actors"] = artist_name
      # movie_details['actor_ids'] = artistid_list
      
    app.logger.debug("Got movie and actor list:{}".format(movie_and_cast))

    return jsonify({
      "success": True,
      "movie_actor_list" : movie_and_cast
    })
  
  @app.route('/moviecast', methods=['POST'])
  @requires_auth('post:moviecast')
  def add_moviecast(payload):
    req_data_dict = json.loads(request.data)
    errno = 0    
    try:
      app.logger.debug("Got request {}".format(req_data_dict))
      if "movie_id" not in req_data_dict or "actor_id" not in req_data_dict:
        errno = 400
        abort(400)
      movie_id = req_data_dict["movie_id"]
      actor_id = req_data_dict["actor_id"]
      logger.debug("Got movie id {} type {}".format(movie_id, type(movie_id)))
      logger.debug("Got actor id {} type {}".format(actor_id, type(actor_id)))    
      mc_single = None
      #Check if this combination of movie and actor exists in database and if it does return
      mc = MovieCast.query.filter_by(movie_id=movie_id).filter_by(artist_id=actor_id).first()
      if mc != None:
        logger.info("Resource already exists in database with requested movie_id {} and actor id {}".format(movie_id, actor_id))
        mc_single = [mc.long()]
      else:
        movie_cast = MovieCast(movie_id = movie_id, artist_id = actor_id)
        movie_cast.insert()
        mc_single = [movie_cast.long()]
      
      return jsonify({
              'moviecast':mc_single,
              'success': True
      })
    except Exception as e:
      app.logger.error("add_moviecast:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno) 

  # @app.route('/moviecast/<mc_id>', methods=['PATCH'])
  # def update_moviecast(mc_id):
  #   app.logger.debug("Moviecast id {}, data {}".format(mc_id, json.loads(request.data)))
  #   errno = 0
    
  #   try:
  #     movie_cast = MovieCast.query.get(mc_id)
  #     if movie_cast == None:
  #       app.logger.debug("No MovieCast found with id {}".format(mc_id))
  #       errno = 404
  #       abort(errno)
  #     body_json = request.get_json()
  #     movie_cast.movie_id = body_json.get('movie_id', movie_cast.movie_id)
  #     movie_cast.artist_id = body_json.get('actor_id', movie_cast.artist_id)
  #     logger.debug("Updated Moviecast {}".format(movie_cast))
  #     movie_cast.update()
  #     return jsonify({
  #             'success': True
  #     })
  #   except Exception as e:
  #     app.logger.error("update_moviecast:Got exception {}".format(e))
  #     if errno == 0:
  #       abort(422)
  #     else:
  #       abort(errno) 

  # @app.route('/moviecast/<mc_id>', methods=['DELETE'])
  # def del_moviecast(mc_id):
  #   app.logger.debug("Got to delete moviecast {}".format(mc_id))
  #   errno = 0
    
  #   try:
  #     mc = MovieCast.query.get(mc_id)
  #     if mc == None:
  #       app.logger.debug("No moviecast found with id {}".format(mc_id))
  #       errno = 404
  #       abort(errno)
  #     mc.delete()
  #     app.logger.debug("moviecast with id {} deleted".format(mc_id))
  #     return jsonify({
  #       'success': True
  #     })
  #   except Exception as e:
  #     app.logger.error("del_moviecast:Got exception {}".format(e))
  #     if errno == 0:
  #       abort(422)
  #     else:
  #       abort(errno)

  @app.route('/moviecast', methods=['DELETE'])
  @requires_auth('delete:moviecast')
  def del_moviecast(payload):
    errno = 0
    logger.debug("Entered")
    req_data_dict = json.loads(request.data)
    app.logger.debug("Got request {}".format(req_data_dict))
    try:
      app.logger.debug("Got request {}".format(req_data_dict))
      if "movie_id" not in req_data_dict or "actor_id" not in req_data_dict:
        errno = 400
        abort(errno)
      movie_id = req_data_dict["movie_id"]
      actor_id = req_data_dict["actor_id"]
      mc = MovieCast.query.filter_by(movie_id=movie_id).filter_by(artist_id=actor_id).first()
      if mc == None:
        logger.error("No resource in database with requested movie_id {} and actor id {}".format(movie_id, actor_id))
        errno = 404
        abort(errno)
      logger.debug ("Deleting {}".format(mc))
      mc.delete()
      return jsonify({
        'success': True
      })
    except Exception as e:
      app.logger.error("del_moviecast:Got exception {}".format(e))
      if errno == 0:
        abort(422)
      else:
        abort(errno)




#Error handlers
#         
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":"resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
    "success": False,
    "error": 422,
    "message":"unprocessable"
  }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
    "success": False,
    "error": 400,
    "message":"bad request"
  }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
    "success": False,
    "error": 405,
    "message":"method not allowed"
  }), 405

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
    "success": False,
    "error": 401,
    "message":"unauthorized for this action"
  }), 401

  @app.errorhandler(AuthError)
  def auth_err_handler(err_obj):
      return jsonify({
      "success": False,
      "error": err_obj.status_code,
      "message":err_obj.error['error']
      }), err_obj.status_code

  return app




app = create_app()

if __name__ == '__main__':
  port = int(os.environ.get("PORT_MOVIE_APP", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)

# app = APP

#Setup logging

if not app.debug:
  #TBD - TO be changed in future version of the software

  #Start of older untested code
  # file_handler = FileHandler('error.log')
  # file_handler.setFormatter(
  #   Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
  # )
  # # Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
  # # Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
  # print("Hehe")
  # app.logger.setLevel(logging.DEBUG)
  # file_handler.setLevel(logging.DEBUG)
  # app.logger.addHandler(file_handler)
  # app.logger.info('errors')
  #End of older untested code
  root = logging.getLogger()
  LOG_LEVEL = os.environ.get('LOG_LEVEL')
  if LOG_LEVEL == "DEBUG":
    root.setLevel(logging.DEBUG)
  else:
    root.setLevel(logging.INFO)
  sh = logging.StreamHandler(sys.stdout)
  if LOG_LEVEL == "DEBUG":
    sh.setLevel(logging.DEBUG)  
  else:
    sh.setLevel(logging.INFO)  

  FORMAT = "[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)0s() ] %(message)s"
  # FORMAT = '[%(asctime)s] p%(process)s {%(pathname)s:%(funcName)1s():%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S'
  formatter = logging.Formatter(FORMAT)
  sh.setFormatter(formatter)
  root.addHandler(sh)
  app.logger = root
  logger = app.logger


else:
  root = logging.getLogger()
  LOG_LEVEL = os.environ.get('LOG_LEVEL')
  if LOG_LEVEL == "DEBUG":
    root.setLevel(logging.DEBUG)
  else:
    root.setLevel(logging.INFO)
  sh = logging.StreamHandler(sys.stdout)
  if LOG_LEVEL == "DEBUG":
    sh.setLevel(logging.DEBUG)  
  else:
    sh.setLevel(logging.INFO)  

  FORMAT = "[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)0s() ] %(message)s"
  # FORMAT = '[%(asctime)s] p%(process)s {%(pathname)s:%(funcName)1s():%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S'
  formatter = logging.Formatter(FORMAT)
  sh.setFormatter(formatter)
  root.addHandler(sh)
  app.logger = root
  logger = app.logger




  # Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
  # Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
  if LOG_LEVEL == "DEBUG":
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)
  logger.debug("First message :)")





