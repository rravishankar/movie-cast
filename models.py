import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
# import logging
# from flask_migrate import Migrate
# from logging import Formatter, FileHandler
from flask_cors import CORS
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


database_name = "movieblitz"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
# user_name = "postgres"
# password = "postgres"
user_name = os.environ.get('MOVIE_DB_USER')
password = os.environ.get('MOVIE_DB_PASSWORD')
database_path = "postgres://{}:{}@{}/{}".format(user_name, password,'localhost:5432', database_name)
ENV = os.environ.get('DEPLOY_MODE')

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = database_path
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
def setup_db(app, database_path=database_path):
  # create and configure the apapp = Flask(__name__)
    # moment = Moment(app)
    # prod_db_uri = os.environ.get("DATABASE_URI")
    # print("prod_db_uri:", prod_db_uri)
    app.config.from_object('config')
    if ENV == 'dev':
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    else:
        prod_db_uri = os.environ.get("DATABASE_URI")
        #IMP Make sure the following lines is commented out
        # print("prod_db_uri", prod_db_uri)
        app.config["SQLALCHEMY_DATABASE_URI"] = prod_db_uri
    db.app = app
    db.init_app(app)
    db.create_all()



class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date())
    mv_association = db.relationship('MovieCast', lazy=True, cascade="all, delete-orphan", backref='Movie')


    def __init__(self, title, release_date):
      self.title = title
      self.release_date = release_date

    def __repr__(self):
        return f'<Movie {self.id} {self.title} {self.release_date}>'
    
    def detail(self):
        return{
            'id' :self.id,
            'title' :self.title,
            # 'genres' : self.genres.split('+'),
            'release_date' :self.release_date
        }
    def short(self):
        return{
            'id':self.id,
            'title':self.title,
        }

    '''
    long()
        long form representation of the Movie model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%A %d. %B %Y")
        }

    
    def insert(self):
        db.app.logger.debug("insert: Inserting movie")
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("insert:Movie Got exception {}".format(e))
            db.session.rollback()
            raise
        # finally:
        #     db.session.expunge(self)
        #     db.session.close()
        #expunge option as suggested in https://docs.sqlalchemy.org/en/13/orm/session_state_management.html#expunging does not work
        #Unable to use object in calling method after calling close
        db.app.logger.info("insert: Inserted movie")

    
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.app.logger.error("update:Movie Got exception {}".format(e))
            db.session.rollback()
            raise
        finally:
            db.session.close()
        db.app.logger.debug("update: Updated movie")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("delete:Movie Got exception {}".format(e))
            db.session.rollback()
            raise
        finally:
            db.session.close()
        db.app.logger.debug("delete: Deleted movie")



class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    mv_association = db.relationship('MovieCast', lazy=True, cascade="all, delete-orphan", backref='artist')

    def __init__(self, name, age, gender):
      self.name = name
      self.age = age
      self.gender = gender

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.age} {self.gender}>'

    def detail(self):
        return{
            'id' :self.id,
            'name' :self.name
        }
    def short(self):
        return{
            'id':self.id,
            'name':self.name
        }

    '''
    long()
        long form representation of the Artist model
    '''
    def long(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'age' :self.age,
            'gender' :self.gender
        }

    def insert(self):
        db.app.logger.debug("insert: Inserting artist")
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("insert:Artist Got exception {}".format(e))
            db.session.rollback()
            raise
        # finally:
        #     db.session.close()
        db.app.logger.info("insert: Inserted Artist")

   
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.app.logger.error("update:Artist Got exception {}".format(e))
            db.session.rollback()
            raise
        finally:
            db.session.close()
        db.app.logger.debug("update: Updated artist")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("delete:Artist Got exception {}".format(e))
            db.session.rollback()
            raise
        finally:
            db.session.close()
        db.app.logger.debug("delete: Deleted artist")


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class MovieCast(db.Model):
    __tablename__ = 'moviecast'
    #Ref https://stackoverflow.com/questions/30406808/flask-sqlalchemy-difference-between-association-model-and-association-table-fo
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    
    def __init__(self,artist_id, movie_id):
      self.artist_id = artist_id
      self.movie_id = movie_id

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("insert:MovieCast Got exception {}".format(e))
            db.session.rollback()
            raise # to raise the exception to caller
        # finally:
            # db.session.close()
        db.app.logger.info("insert:MovieCast inserted")


    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.app.logger.error("update:MovieCast Got exception {}".format(e))
            db.session.rollback()
            raise # to raise the exception to caller
        finally:
            db.session.close()
        db.app.logger.info("update:MovieCast updated")
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.app.logger.error("delete:MoviCast Got exception {}".format(e))
            db.session.rollback()
            raise # to raise the exception to caller
        finally:
            db.session.close()
        db.app.logger.info("delete:MoviCast Deleted")

    '''
    long()
        long form representation of the Artist model
    '''
    def long(self):
        return {
            'id' :self.id,
            'movie_id' :self.movie_id,
            'artist_id' :self.artist_id
        }

    def __repr__(self):
        return f'<MovieCast {self.id} {self.artist_id} {self.movie_id} >'
