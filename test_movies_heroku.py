import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Artist, MovieCast
import requests
import responses

exec_prod_token = os.environ.get("EXEC_PRODUCER_TOKEN")
casting_director_token = os.environ.get("CASTING_DIRECTOR_TOKEN")
casting_assistant_token = os.environ.get("CASTING_ASSISTANT_TOKEN")

access_token = exec_prod_token

auth_header = {'Authorization': access_token}

inserted_movie_id = 0
inserted_actor_id = 0

url = "https://movie-dig.herokuapp.com"
# url = "http://127.0.0.1"


class MovieTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_app()
        # self.client = self.app.test_client
        # self.database_name = "movie_test"
        # # self.database_path = "postgres://{}/{}".format('localhost:5432',\
        #  self.database_name)
        # self.database_path = "postgres://{}:{}@{}/{}".format('postgres', \
        # 'postgres', 'localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)
        # self.new_que = {
        #     'question':'What color is space?',
        #     'answer': 'Good question',
        #     'difficulty': 5,
        #     'category': 5
        # }

        # binds the app to the current context
        # with self.app.app_context():
        # self.db = SQLAlchemy()
        # self.db.init_app(self.app)
        # # create all tables
        # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# Test for movies

    def test_get_paginated_movies(self):
        # resp = self.client().get('/movies?page=5', headers=auth_header)
        resp = requests.get(url + '/movies', headers=auth_header)
        data = resp.json()
        print("test_get_paginated_movies: Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        # page_num = 1
        # while 1:
        #     resp = self.client().get('/movies?page=' +str(page_num), \
        # headers=auth_header)
        #     data = json.loads(resp.data)
        #     if data['success'] == False:
        #         break
        #     print("Movie data (page {}):{}".format(page_num,data['movies']))
        #     page_num += 1

    def test_404_get_request_beyond_validate_page_movies(self):
        resp = requests.get(url + '/movies?page=100000', headers=auth_header)
        # resp = self.client().get('/movies?page=100000', headers=auth_header)
        data = resp.json()
        print("test_404_sent_request_beyond_validate_page_movies:\
            Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_movie(self):
        global inserted_movie_id, auth_header
        new_header = auth_header.copy()
        # resp = self.client().post('/movies', json='{"title": "Geography",\
        # "release_date":"2010/02/16"}', headers=auth_header)
        new_header["Content-type"] = "application/json"
        resp = requests.post(
            url + '/movies',
            data='{"title": "Heroku Geography Super",\
                "release_date":"2010/02/16"}',
            headers=new_header)
        data = resp.json()
        print("test_add_movie: Got response:{}".format(data))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        movie_details_dict = data['movies'][0]
        print("test_add_movie: Got movie_details_dict:", movie_details_dict)
        inserted_movie_id = movie_details_dict["id"]

    def test_400_error_add_movie_without_details(self):
        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        resp = requests.post(
            url + '/movies',
            data='{"release_date":"2010/02/16"}',
            headers=new_header)
        data = resp.json()
        print("test_400_error_add_movie_without_details: Got response:\
            {}".format(data))

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_movie(self):
        global inserted_movie_id
        self.test_add_movie()
        movie_id = inserted_movie_id
        print("test_delete_movie:Trying to delete movie", movie_id)
        # Not needed, as this doesn't have data
        new_header = auth_header.copy()
        resp = requests.delete(
            url + '/movies/' + str(movie_id),
            headers=new_header)
        data = resp.json()
        print("test_delete_movie:Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_if_movie_does_not_exist(self):
        new_header = auth_header.copy()  # Not needed

        self.test_delete_movie()
        # This will be the delete movie ID
        deleted_movie_id = inserted_movie_id
        resp = requests.delete(
            url + '/movies/' + str(deleted_movie_id),
            headers=new_header)
        data = resp.json()
        print("test_404_delete_if_movie_does_not_exist:Got response", data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie(self):
        global inserted_movie_id
        self.test_add_movie()
        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"
        print("test_update_movie: Got inserted movie id: \
            {}".format(inserted_movie_id))
        resp = requests.patch(
            url + '/movies/' + str(inserted_movie_id),
            data='{"title":"History"}',
            headers=new_header)
        data = resp.json()
        print("test_update_movie:Got response", data)
        self.assertEqual(data['success'], True)
        self.test_get_paginated_movies()

    def test_404_update_movie_not_existing(self):
        global inserted_movie_id
        self.test_delete_movie()
        print("test_404_update_movie_not_existing: Got inserted & \
            deleted movie id: {}".format(
            inserted_movie_id))

        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        resp = requests.patch(
            url + '/movies/' + str(inserted_movie_id),
            data='{"title":"History"}',
            headers=new_header)
        data = resp.json()
        print("test_404_update_movie_not_existing:Got response", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# #Test for actors/artist

    def test_get_paginated_actors(self):
        resp = requests.get(url + '/actors?page=2', headers=auth_header)
        # resp = self.client().get('/actors', headers=auth_header)
        data = resp.json()
        print("test_get_paginated_actors: Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        # page_num = 1
        # while 1:
        #     resp = self.client().get('/actors?page=' +str(page_num),
        # headers=auth_header)
        #     data = json.loads(resp.data)
        #     if data['success'] == False:
        #         break
        #     print("Actor data (page {}):{}".format(page_num,data['actors']))
        #     page_num += 1

    def test_404_get_request_beyond_validate_page_actors(self):
        resp = requests.get(url + '/actors?page=200000', headers=auth_header)
        data = resp.json()
        print("test_404_get_request_beyond_validate_page_actors:\
             Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_actor(self):
        global inserted_actor_id, auth_header
        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        resp = requests.post(
            url + '/actors',
            data='{"name":"Dorumcorum","age":"33", "gender": "Male"}',
            headers=new_header)
        data = resp.json()
        print("test_add_actor: Got response:{}".format(data))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        actor_details_dict = data['actors'][0]
        print("test_add_actor: Got actor_details_dict:", actor_details_dict)
        inserted_actor_id = actor_details_dict["id"]

    def test_400_error_add_actor_without_details(self):
        global inserted_actor_id, auth_header
        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        resp = requests.post(
            url + '/actors',
            data='{"name":"Incompo","gender": "Male"}',
            headers=new_header)
        data = resp.json()
        print("test_400_error_add_actor_without_details: Got response", data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_actor(self):
        global inserted_actor_id
        self.test_add_actor()
        actor_id = inserted_actor_id
        print("test_delete_actor:Trying to delete actor", actor_id)

        resp = requests.delete(
            url + '/actors/' + str(actor_id),
            headers=auth_header)
        data = resp.json()
        print("test_delete_actor: Got response", data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_if_actor_does_not_exist(self):
        self.test_delete_actor()
        deleted_actor_id = inserted_actor_id
        resp = requests.delete(
            url + '/actors/' + str(deleted_actor_id),
            headers=auth_header)
        data = resp.json()
        print("test_404_delete_if_actor_does_not_exist: Got response", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        global inserted_actor_id
        self.test_add_actor()
        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"
        print("test_update_actor: Got inserted actor id:\
             {}".format(inserted_actor_id))
        resp = requests.patch(
            url +
            '/actors/' +
            str(inserted_actor_id),
            data='{"name":"God"}',
            headers=new_header)
        data = resp.json()
        print("test_update_actor: Got response", data)
        self.assertEqual(data['success'], True)
        self.test_get_paginated_actors()

    def test_404_update_actor_not_existing(self):
        global inserted_actor_id
        self.test_delete_actor()
        print("test_404_update_actor_not_existing: \
            Got inserted actor id: {}".format(
            inserted_actor_id))

        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        resp = requests.patch(
            url + '/actors/' + str(inserted_actor_id),
            data='{"title":"History Civics"}',
            headers=new_header)
        data = resp.json()
        print("test_404_update_actor_not_existing: Got response", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_moviecast(self, auth_header_farg=None):
        global inserted_actor_id, inserted_movie_id
        self.test_add_actor()
        self.test_add_movie()
        auth_header_final = None
        if auth_header_farg is None:
            auth_header_final = auth_header
        else:
            auth_header_final = auth_header_farg

        new_header = auth_header_final.copy()
        new_header["Content-type"] = "application/json"

        print(
            "test_add_moviecast: Got inserted actor id: {} \
                movie_id: {}".format(
                inserted_actor_id,
                inserted_movie_id))
        resp = requests.post(
            url +
            '/moviecast',
            data='{"actor_id":' +
            str(inserted_actor_id) +
            ',' +
            '"movie_id":' +
            str(inserted_movie_id) +
            '}',
            headers=new_header)
        data = resp.json()
        print("test_add_moviecast: Got response:{}".format(data))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        moviecast_details_dict = data['moviecast'][0]
        print(
            "test_add_movie: Got actor_details_dict:",
            moviecast_details_dict)

    def test_400_error_add_moviecast_without_details(self):
        global inserted_actor_id, inserted_movie_id
        self.test_add_actor()

        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"

        print("test_400_error_add_moviecast_without_details: \
            Got inserted actor id: {} ".format(
            inserted_actor_id))
        resp = requests.post(
            url + '/moviecast',
            data='{"actor_id":' + str(inserted_actor_id) + '}',
            headers=new_header)
        data = resp.json()
        print(
            "test_400_error_add_moviecast_without_details: \
                Got response:{}".format(data))

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_moviecast(self):
        global inserted_actor_id, inserted_movie_id, auth_header
        self.test_add_moviecast()
        print(
            "test_delete_moviecast: Deleting actor id: {} movie_id: {}".format(
                inserted_actor_id,
                inserted_movie_id))

        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"
        resp = requests.delete(
            url +
            '/moviecast',
            data='{"actor_id":' +
            str(inserted_actor_id) +
            ',' +
            '"movie_id":' +
            str(inserted_movie_id) +
            '}',
            headers=new_header)
        data = resp.json()

        print("test_delete_moviecast: Got response:{}".format(data))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_if_moviecast_does_not_exist(self):
        print(
            "test_404_delete_if_moviecast_does_not_exist: Deleting \
                actor id: {} movie_id: {}".format(
                0,
                0))

        new_header = auth_header.copy()
        new_header["Content-type"] = "application/json"
        resp = requests.delete(
            url + '/moviecast',
            data='{"actor_id":' + str(0) + ',' + '"movie_id":' + str(0) + '}',
            headers=new_header)
        data = resp.json()

        print("test_404_delete_if_moviecast_does_not_exist: Got \
            response", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_role_casting_assistant_not_allowed_add_moviecast(self):
        global inserted_actor_id, inserted_movie_id, casting_assistant_token
        print("test_role_casting_assistant_not_allowed_add_moviecast: Entered")
        new_header = {'Authorization': casting_assistant_token}
        new_header["Content-type"] = "application/json"

        print(
            "test_role_casting_assistant_not_allowed_add_moviecast: Got \
                inserted actor id: {} movie_id: {}".format(
                inserted_actor_id,
                inserted_movie_id))
        resp = requests.post(
            url +
            '/moviecast',
            data='{"actor_id":' +
            str(inserted_actor_id) +
            ',' +
            '"movie_id":' +
            str(inserted_movie_id) +
            '}',
            headers=new_header)

        data = resp.json()
        print(
            "test_role_casting_assistant_not_allowed_add_moviecast:Got \
                response",
            data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_role_casting_assistant_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, casting_assistant_token
        print("test_role_casting_assistant_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': casting_assistant_token}

        resp = requests.get(url + '/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = resp.json()
        print("test_role_casting_assistant_allowed_to_get_actors: \
            Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_role_casting_dir_not_allowed_add_moviecast(self):
        global inserted_actor_id, inserted_movie_id, casting_director_token
        print("test_role_casting_dir_not_allowed_add_moviecast: Entered")
        auth_header_ca = {'Authorization': casting_director_token}
        auth_header_ca["Content-type"] = "application/json"

        print("test_role_casting_dir_not_allowed_add_moviecast: Got inserted \
            actor id: {} movie_id: \
                {}".format(inserted_actor_id, inserted_movie_id))
        resp = requests.post(
            url +
            '/moviecast',
            data='{"actor_id":' +
            str(inserted_actor_id) +
            ',' +
            '"movie_id":' +
            str(inserted_movie_id) +
            '}',
            headers=auth_header_ca)
        data = resp.json()
        print("test_role_casting_dir_not_allowed_add_moviecast:Got data", data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_role_casting_dir_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, casting_director_token
        print("test_role_casting_dir_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': casting_director_token}

        resp = requests.get(url + '/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = resp.json()
        print("test_role_casting_dir_allowed_to_get_actors: \
            Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_role_exec_prod_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, exec_prod_token
        print("test_role_exec_prod_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': exec_prod_token}

        resp = requests.get(url + '/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = resp.json()
        print("test_role_exec_prod_allowed_to_get_actors: Got response", data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_role_exec_prod_allowed_to_add_movie(self):
        global inserted_movie_id
        auth_header_ca = {'Authorization': exec_prod_token}
        auth_header_ca["Content-type"] = "application/json"

        resp = requests.post(url + '/movies', data='{"title": \
            "Geography","release_date":"2010/02/16"}', headers=auth_header_ca)
        data = resp.json()

        print("test_role_exec_prod_allowed_to_add_movie: Got\
             response:{}".format(data))
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        movie_details_dict = data['movies'][0]
        print("test_role_exec_prod_allowed_to_add_movie: Got \
            movie_details_dict:", movie_details_dict)
        inserted_movie_id = movie_details_dict["id"]

    def test_get_paginated_moviecast(self):
        # resp = self.client().get('/movies?page=5', headers=auth_header)
        resp = requests.get(url + '/moviecast')
        data = resp.json()
        print("test_get_paginated_moviecast: Got response:{}".format(data))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_actor_list'])

    def test_404_get_request_beyond_validate_page_moviecast(self):
        resp = requests.get(url + '/moviecast?page=100000')
        data = resp.json()
        print("test_404_get_request_beyond_validate_page_moviecast:\
            Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    """
    TODO
    Write at least one test for each test for successful operation and
    for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
