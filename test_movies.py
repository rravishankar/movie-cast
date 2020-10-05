import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Artist, MovieCast

exec_prod_token = os.environ.get("EXEC_PRODUCER_TOKEN")
casting_director_token = os.environ.get("CASTING_DIRECTOR_TOKEN")
casting_assistant_token = os.environ.get("CASTING_ASSISTANT_TOKEN")
# casting_director_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtYa29NcnIwMUd6bS1GMHZqZER0USJ9.eyJpc3MiOiJodHRwczovL2NyYWxpbmEtdGVzdC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk1NzY2MTEyOTcyMzQ4NDU0NjQiLCJhdWQiOlsibW92aWUiLCJodHRwczovL2NyYWxpbmEtdGVzdC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxNTU0MjQ2LCJleHAiOjE2MDE1NjE0NDYsImF6cCI6Ik40MDdTc3FIakV0QW9aSWVYYzRCTmtBdHRhS2lOeVR5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.NqzgJ-D2m8HjbVXwY4WQdMIGlpISfPoscmkqVV78In5qRQAQQtbzXytG9_0sN8u6TSx4chzAVvsI2EGKCJT2q9dZB1mzw9X0y3MD6cwMJ8aYbML4jjWDunP0BrVgyEvQVK8RY89UWXjj7OP_q4JaDkQHrYC54Z0F1-Ts0JYDLYXqz_JpCCtHpXLn48PHsVxmHJnN9bLAJF7pPZbhWWpHzy1k1fk9hXMYJe9uQtT8hDIi23LNO_huFOm6xhzloBuxpuCAKdeEEQYTTzuFS7zBi1XSYh9SDgWFVW_pTlU4HjqFDfDccqk6XkvQ9jr8RkIEeqFHQe9dN5TrRbSjBV4EiQ"

access_token = exec_prod_token

auth_header = {'Authorization': access_token}

inserted_movie_id = 0
inserted_actor_id = 0

class MovieTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movie_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)        
        setup_db(self.app, self.database_path)
        # self.new_que = {
        #     'question':'What color is space?',
        #     'answer': 'Good question',
        #     'difficulty': 5,
        #     'category': 5
        # }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


#Test for movies
    def test_get_paginated_movies(self):
        # resp = self.client().get('/movies?page=5', headers=auth_header)
        resp = self.client().get('/movies', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        # page_num = 1
        # while 1:
        #     resp = self.client().get('/movies?page=' +str(page_num), headers=auth_header)
        #     data = json.loads(resp.data)
        #     if data['success'] == False:
        #         break
        #     print("Movie data (page {}):{}".format(page_num,data['movies']))
        #     page_num += 1
            
    
    def test_404_get_request_beyond_validate_page_movies(self):
        resp = self.client().get('/movies?page=100000', headers=auth_header)
        data = json.loads(resp.data)
        print("test_404_sent_request_beyond_validate_page_movies:Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_movie(self):
        global inserted_movie_id
        # resp = self.client().post('/movies', json='{"title": "Geography","release_date":"2010/02/16"}', headers=auth_header)
        resp = self.client().post('/movies', data='{"title": "Geography","release_date":"2010/02/16"}', content_type='application/json', headers=auth_header)
        print("test_add_movie: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        movie_details_dict = data['movies'][0]
        print("test_add_movie: Got movie_details_dict:",movie_details_dict)
        inserted_movie_id = movie_details_dict["id"]

    def test_400_error_add_movie_without_details(self):
        resp = self.client().post('/movies', data='{"release_date":"2010/02/16"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')    
    
    def test_delete_movie(self):
        global inserted_movie_id
        self.test_add_movie()
        movie_id = inserted_movie_id
        print("test_delete_movie:Trying to delete movie", movie_id)
        resp = self.client().delete('/movies/' + str(movie_id), headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_if_movie_does_not_exist(self):
        resp = self.client().delete('/movies/100000',headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    def test_update_movie(self):
        global inserted_movie_id
        self.test_add_movie()
        print("test_update_movie: Got inserted movie id: {}".format(inserted_movie_id))
        resp = self.client().patch('/movies/' + str(inserted_movie_id), data='{"title":"History"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(data['success'], True)
        self.test_get_paginated_movies()

    def test_404_update_movie_not_existing(self):
        global inserted_movie_id
        self.test_add_movie()
        print("test_404_update_movie_not_existing: Got inserted movie id: {}".format(inserted_movie_id))
        self.test_delete_movie()
        resp = self.client().patch('/movies/' + str(inserted_movie_id), data='{"title":"History"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


#Test for actors/artist
    def test_get_paginated_actors(self):
        resp = self.client().get('/actors?page=2', headers=auth_header)
        # resp = self.client().get('/actors', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        # page_num = 1
        # while 1:
        #     resp = self.client().get('/actors?page=' +str(page_num), headers=auth_header)
        #     data = json.loads(resp.data)
        #     if data['success'] == False:
        #         break
        #     print("Actor data (page {}):{}".format(page_num,data['actors']))
        #     page_num += 1
        
    
    def test_404_get_request_beyond_validate_page_actors(self):
        resp = self.client().get('/actors?page=1000', headers=auth_header)
        data = json.loads(resp.data)
        print("test_404_get_request_beyond_validate_page_actors:Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_add_actor(self):
        global inserted_actor_id
        resp = self.client().post('/actors', data='{"name":"Dorumcorum","age":"33", "gender": "Male"}', content_type='application/json', headers=auth_header)
        print("test_add_actor: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        actor_details_dict = data['actors'][0]
        print("test_add_actor: Got actor_details_dict:",actor_details_dict)
        inserted_actor_id = actor_details_dict["id"]

    def test_400_error_add_actor_without_details(self):
        resp = self.client().post('/actors', data='{"name":"Half"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') 

    def test_delete_actor(self):
        global inserted_actor_id
        self.test_add_actor()
        actor_id = inserted_actor_id
        print("test_delete_actor:Trying to delete actor", actor_id)
        resp = self.client().delete('/actors/' + str(actor_id), headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_if_actor_does_not_exist(self):
        resp = self.client().delete('/actors/100000',headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    def test_update_actor(self):
        global inserted_actor_id
        self.test_add_actor()
        print("test_update_actor: Got inserted actor id: {}".format(inserted_actor_id))
        resp = self.client().patch('/actors/' + str(inserted_actor_id), data='{"name":"God"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(data['success'], True)
        self.test_get_paginated_actors()

    def test_404_update_actor_not_existing(self):
        global inserted_actor_id
        self.test_add_actor()
        print("test_404_update_actor_not_existing: Got inserted actor id: {}".format(inserted_actor_id))
        self.test_delete_actor()
        resp = self.client().patch('/actors/' + str(inserted_actor_id), data='{"title":"History"}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_add_moviecast(self, auth_header_farg=None):
        global inserted_actor_id, inserted_movie_id
        self.test_add_actor()
        self.test_add_movie()
        auth_header_final = None 
        if auth_header_farg == None:
            auth_header_final = auth_header
        else:
            auth_header_final = auth_header_farg


        print("test_add_moviecast: Got inserted actor id: {} movie_id: {}".format(inserted_actor_id, inserted_movie_id))
        resp = self.client().post('/moviecast', data='{"actor_id":' + str(inserted_actor_id) + ',' + '"movie_id":' + str(inserted_movie_id) +  '}', content_type='application/json', headers=auth_header_final)
        print("test_add_actor: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        moviecast_details_dict = data['moviecast'][0]
        print("test_add_movie: Got actor_details_dict:",moviecast_details_dict)


    def test_400_error_add_moviecast_without_details(self):
        resp = self.client().post('/moviecast', data='{"actor_id":' + str(inserted_actor_id) + '}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') 

    def test_delete_moviecast(self):
        global inserted_actor_id, inserted_movie_id
        self.test_add_moviecast()
        print("test_delete_moviecast: Deleting actor id: {} movie_id: {}".format(inserted_actor_id, inserted_movie_id))
        resp = self.client().delete('/moviecast', data='{"actor_id":' + str(inserted_actor_id) + ',' + '"movie_id":' + str(inserted_movie_id) +  '}', content_type='application/json', headers=auth_header)
        print("test_delete_moviecast: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_404_delete_if_moviecast_does_not_exist(self):
        print("test_404_delete_if_moviecast_does_not_exist: Deleting actor id: {} movie_id: {}".format(0, 0))
        resp = self.client().delete('/moviecast', data='{"actor_id":' + str(0) + ',' + '"movie_id":' + str(0) +  '}', content_type='application/json', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_role_casting_assistant_not_allowed_add_moviecast(self):
        global inserted_actor_id, inserted_movie_id, casting_assistant_token
        print("test_role_casting_assistant_not_allowed_add_moviecast: Entered")
        auth_header_ca = {'Authorization': casting_assistant_token}

        print("test_role_casting_assistant_not_allowed_add_moviecast: Got inserted actor id: {} movie_id: {}".format(inserted_actor_id, inserted_movie_id))
        resp = self.client().post('/moviecast', data='{"actor_id":' + str(inserted_actor_id) + ',' + '"movie_id":' + str(inserted_movie_id) +  '}', content_type='application/json', headers=auth_header_ca)
        print("test_role_casting_assistant_not_allowed_add_moviecast: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        print("test_role_casting_assistant_not_allowed_add_moviecast:Got data", data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_role_casting_assistant_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, casting_assistant_token
        print("test_role_casting_assistant_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': casting_assistant_token}

        resp = self.client().get('/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_role_casting_dir_not_allowed_add_moviecast(self):
        global inserted_actor_id, inserted_movie_id, casting_director_token
        print("test_role_casting_dir_not_allowed_add_moviecast: Entered")
        auth_header_ca = {'Authorization': casting_director_token}

        print("test_role_casting_dir_not_allowed_add_moviecast: Got inserted actor id: {} movie_id: {}".format(inserted_actor_id, inserted_movie_id))
        resp = self.client().post('/moviecast', data='{"actor_id":' + str(inserted_actor_id) + ',' + '"movie_id":' + str(inserted_movie_id) +  '}', content_type='application/json', headers=auth_header_ca)
        print("test_role_casting_dir_not_allowed_add_moviecast: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        print("test_role_casting_dir_not_allowed_add_moviecast:Got data", data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(data['success'], False)
        
    def test_role_casting_dir_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, casting_director_token
        print("test_role_casting_dir_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': casting_director_token}

        resp = self.client().get('/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
        
    def test_role_exec_prod_allowed_to_get_actors(self):
        global inserted_actor_id, inserted_movie_id, exec_prod_token
        print("test_role_exec_prod_allowed_to_get_actors: Entered")
        auth_header_ca = {'Authorization': exec_prod_token}

        resp = self.client().get('/actors', headers=auth_header_ca)
        # resp = self.client().get('/actors', headers=auth_header)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    def test_role_exec_prod_allowed_to_add_movie(self):
        global inserted_movie_id
        auth_header_ca = {'Authorization': exec_prod_token}
        resp = self.client().post('/movies', data='{"title": "Geography","release_date":"2010/02/16"}', content_type='application/json', headers=auth_header_ca)

        print("test_role_exec_prod_allowed_to_add_movie: Got response:{} {}".format(resp.data, type(resp.data)))
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        movie_details_dict = data['movies'][0]
        print("test_role_exec_prod_allowed_to_add_movie: Got movie_details_dict:",movie_details_dict)
        inserted_movie_id = movie_details_dict["id"]

    def test_get_paginated_moviecast(self):
        # resp = self.client().get('/movies?page=5', headers=auth_header)
        resp = self.client().get('/moviecast')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_actor_list'])
        page_num = 1
        # while 1:
        #     resp = self.client().get('/moviecast?page=' +str(page_num))
        #     data = json.loads(resp.data)
        #     if data['success'] == False:
        #         break
        #     print("Moviecast data (page {}):{}".format(page_num,data['movie_actor_list']))
        #     page_num += 1
            
    
    def test_404_get_request_beyond_validate_page_moviecast(self):
        resp = self.client().get('/moviecast?page=100000')
        data = json.loads(resp.data)
        print("test_404_get_request_beyond_validate_page_moviecast:Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')





    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()