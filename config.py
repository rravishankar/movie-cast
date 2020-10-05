import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
