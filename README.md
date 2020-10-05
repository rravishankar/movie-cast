#### Permissions and Roles

With ref to the actors and movies we have the following permissions which are self explanatory 


###### Permissions

get:actors

post:actors

delete:actors

update:actors

get:movies

post:movies

delete:movies

update:movies


The following permissions are for adding/deleting  a combination of movie and actors

post:moviecast

delete:moviecast

One can get a list of current movie-cast combinations too. There is no authentication/permission required for getting a list of movie-cast combination - all roles and do it.

###### Roles and respective permissions:

Casting Assistant:

get:actors

get:movies



Casting Director:

get:actors

get:movies

post:actors

delete:actors

update:actors

update:movies



Executive Producer:

get:actors

get:movies

post:actors

delete:actors

update:actors

update:movies

post:movies

delete:movies

(Additional)

post:moviecast

delete:moviecast



#### Requests and Responses

Please note that all requests need to be added authentication to the requests - the examples below DO NOT ADD THE AUTHENTICATION HEADER for reasons of breivity. The actual request needs to have the same like the following:

e.g. : 



---Start of sample request and response---

$ export EXEC_PRODUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtYa29NcnIwMUd6bS1GMHZqZER0USJ9.eyJpc3MiOiJodHRwczovL2NyYWxpbmEtdGVzdC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk1NzY2MTEyOTcyMzQ4NDU0NjQiLCJhdWQiOlsibW92aWUiLCJodHRwczovL2NyYWxpbmEtdGVzdC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxNjI5NzM3LCJleHAiOjE2MDE2MzY5MzcsImF6cCI6Ik40MDdTc3FIakV0QW9aSWVYYzRCTmtBdHRhS2lOeVR5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVjYXN0IiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllY2FzdCIsInBvc3Q6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.nO0r-icZjNLXnh770-v6PBQpDov9Ar6j0wZf5RR5bhgtqb8R7LjjDol5Zjhq2UQvTEI1ExgmZTUwb4qrxtWNQO4vnvtntxG3ys1wnK0DQZpzftwY9XFuKLQXqmwIPlPmfTEoD4zq45QNrUbSmI4TF1YA1bRtHs3ygzdFA0q6CvVmrP5G_H0w_j9Wj5QXQmWqe0OlBijbeoSi5wunbHBLEvewefcPYxA9jN7nhASBmd3UzNQy0qqfFwBUqiVKzwjeOQhDqZ2y1__Q0C6omqgDQgc9ByqwqyGcs8c7_vHpaGFjP9XcnplplaG0zK6fe_U7Rn2pysULe3zRVBtOqQzsQA"

$ curl --request POST -d '{"actor_id":3, "movie_id":4}' -H "Content-Type: application/json" http://127.0.0.1:5000/moviecast -H "Authorization: Bearer ${EXEC_PRODUCER_TOKEN}"
{
  "moviecast": [
    {
      "artist_id": 3, 
      "id": 26, 
      "movie_id": 4
    }
  ], 
  "success": true
}

---End of sample request and response---



The part in the command *-H "Authorization: Bearer ${EXEC_PRODUCER_TOKEN}"* needs to be added to each of the commands as required.



- Get all actors 
  Request: $ curl --request GET 'http://127.0.0.1:5000/actors'
  {
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      }
    }, 
    "success": true
  }

  Support for pagination (current page size = 5):
   $ curl --request GET 'http://127.0.0.1:5000/actors?page=1'
  {
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "9": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "10": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "11": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }
    }, 
    "success": true
  }
  (env) $ curl --request GET 'http://127.0.0.1:5000/actors?page=2'
  {
    "actors": {
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      }, 
      "13": {
        "age": 33, 
        "gender": "Male", 
        "name": "Ginger"
      }
    }, 
    "success": true
  }
  
- Insert an actor

  Request: 
  curl -d '{"name":"Abhishek","age":"33", "gender":"Male"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/actors

  Response:

  {
  "success": true
  }

  Trying to add actor with incomplete details:

  $curl -d '{"name":"Abhishek","age":"33"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/actors
  {
    "error": 400, 
    "message": "bad request", 
    "success": false
  }

  

- Update actor

  $ curl --request GET 'http://127.0.0.1:5000/actors'
  {
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      }, 
      "9": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "10": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "11": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "13": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }
    }, 
    "success": true
  }
  Modify actor with id 13:

  $curl -d '{"name":"Ginger"}' -H "Content-Type: application/json" -X PATCH 127.0.0.1:5000/actors/13
  {
    "success": true
  }
  $ curl --request GET 'http://127.0.0.1:5000/actors'
  {
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      }, 
      "9": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "10": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "11": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }, 
      "13": {
        "age": 33, 
        "gender": "Male", 
        "name": "Ginger"
      }
    }, 
    "success": true
  }

  

- Get all movies

  $ curl --request GET 'http://127.0.0.1:5000/movies'
  {
    "movies": {
      "1": {
        "release_date": "Sunday 05. February 1978", 
        "title": "Great Escape"
      }, 
      "2": {
        "release_date": "Thursday 05. April 1979", 
        "title": "The Scape"
      }, 
      "3": {
        "release_date": "Thursday 05. April 1979", 
        "title": "Right"
      }, 
      "4": {
        "release_date": "Saturday 02. January 1988", 
        "title": "Superman"
      }, 
      "27": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GCMail"
      }, 
      "28": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "CalCMail"
      }, 
      "29": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCMail"
      }, 
      "30": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCCCMail"
      }, 
      "31": {
        "release_date": "Thursday 08. July 1999", 
        "title": "Gel"
      }
    }, 
    "success": true
  }

- Get movies with details of cast, release date
  Request:
  curl --request GET 'http://127.0.0.1:5000/moviecast'
  Response:
  {
  "movie_actor_list": [
    {
      "Actors": "Amitabh, Aamir", 
      "Release Date": "Sunday 05. February 1978", 
      "Title": "Great Escape"
    }, 
    {
      "Actors": "Aamir", 
      "Release Date": "Saturday 02. January 1988", 
      "Title": "Superman"
    }
  ], 
  "success": true
  }

Support for pagination:

$ curl --request GET 'http://127.0.0.1:5000/movies?page=1'
{
  "movies": {
    "27": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "GCMail"
    }, 
    "28": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "CalCMail"
    }, 
    "29": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "GelCMail"
    }, 
    "30": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "GelCCCMail"
    }, 
    "35": {
      "release_date": "Tuesday 02. February 2010", 
      "title": "Best"
    }
  }, 
  "success": true
}
(env) $ curl --request GET 'http://127.0.0.1:5000/movies?page=2'
{
  "movies": {
    "1": {
      "release_date": "Sunday 05. February 1978", 
      "title": "Great Escape"
    }, 
    "3": {
      "release_date": "Thursday 05. April 1979", 
      "title": "Right"
    }, 
    "4": {
      "release_date": "Saturday 02. January 1988", 
      "title": "Superman"
    }, 
    "32": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "Jojo"
    }, 
    "33": {
      "release_date": "Tuesday 08. June 1999", 
      "title": "Jojo11"
    }
  }, 
  "success": true
}

- Delete actor with deletion of corresponding items in moviecast table:
  Request-response:$ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir, Abhishek", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Abhishek", 
        "Release Date": "Thursday 05. April 1979", 
        "Title": "The Scape"
      }, 
      {
        "Actors": "Abhishek", 
        "Release Date": "Thursday 05. April 1979", 
        "Title": "Right"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }
    ], 
    "success": true
  }

  Request-response all actors list:
  $ curl --request GET 'http://127.0.0.1:5000/actors'{
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      },

  "8": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }  

  }, 
    "success": true
  }

  Delete request and response:
  $ curl http://127.0.0.1:5000/actors/8 -X DELETE
  {
    "success": true
  }

  Post delete status of actors and moviecast table:

  $ curl --request GET 'http://127.0.0.1:5000/actors'{
    "actors": {
      "1": {
        "age": 73, 
        "gender": "Male", 
        "name": "Amitabh"
      }, 
      "2": {
        "age": 55, 
        "gender": "Male  ", 
        "name": "Aamir"
      }, 
      "3": {
        "age": 35, 
        "gender": "Female", 
        "name": "Jugnu"
      }, 
      "4": {
        "age": 70, 
        "gender": "Female", 
        "name": "Hema"
      }
    }, 
    "success": true
  }

  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }
    ], 
    "success": true
  }

  Pagination support:$ curl --request GET 'http://127.0.0.1:5000/moviecast?page=1'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }
    ], 
    "success": true
  }
  
- Add a movie:

  $ curl -d '{"title": "Geography","release_date":"2010/02/16"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/movies
  {
    "movies": [
      {
        "id": 36, 
        "release_date": "Tuesday 16. February 2010", 
        "title": "Geography"
      }
    ], 
    "success": true
  }

- Movie deletion :

  $ curl http://127.0.0.1:5000/movies/25 -X DELETE
  {
    "success": true
  }

  

  Trying to delete a movie ID not in database:
  $ curl http://127.0.0.1:5000/movies/25 -X DELETE
  {
    "error": 404, 
    "message": "resource not found", 
    "success": false
  }

  Effect of delete movie on moviecast:

  

  First add a movie :

  $ curl -d '{"title": "Geography","release_date":"2010/02/16"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/movies
  {
    "movies": [
      {
        "id": 36, 
        "release_date": "Tuesday 16. February 2010", 
        "title": "Geography"
      }
    ], 
    "success": true
  }

  Add a moie - actor pair

  $ curl -d '{"movie_id":36,"actor_id":2}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/moviecast
  {
    "moviecast": [
      {
        "artist_id": 2, 
        "id": 22, 
        "movie_id": 36
      }
    ], 
    "success": true
  }

  

  

  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Tuesday 16. February 2010", 
        "Title": "Geography"
      }
    ], 
    "success": true
  }

  

   curl http://127.0.0.1:5000/movies/36 -X DELETE
  {
    "success": true
  }
  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }
    ], 
    "success": true
  }

- Movie updation: $ curl --request GET 'http://127.0.0.1:5000/movies'
  {
    "movies": {
      "1": {
        "release_date": "Sunday 05. February 1978", 
        "title": "Great Escape"
      }, 
      "2": {
        "release_date": "Thursday 05. April 1979", 
        "title": "The Scape"
      }, 
      "3": {
        "release_date": "Thursday 05. April 1979", 
        "title": "Right"
      }, 
      "4": {
        "release_date": "Saturday 02. January 1988", 
        "title": "Superman"
      }, 
      "27": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GCMail"
      }, 
      "28": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "CalCMail"
      }, 
      "29": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCMail"
      }, 
      "30": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCCCMail"
      }, 
      "31": {
        "release_date": "Thursday 08. July 1999", 
        "title": "Gel"
      }
    }, 
    "success": true
  }

  $  curl -d '{"title":"Gelly","release_date":"1999-06-08"}' -H "Content-Type: application/json" -X PATCH 127.0.0.1:5000/movies/31
  {
    "success": true
  }
  $ curl --request GET 'http://127.0.0.1:5000/movies'
  {
    "movies": {
      "1": {
        "release_date": "Sunday 05. February 1978", 
        "title": "Great Escape"
      }, 
      "2": {
        "release_date": "Thursday 05. April 1979", 
        "title": "The Scape"
      }, 
      "3": {
        "release_date": "Thursday 05. April 1979", 
        "title": "Right"
      }, 
      "4": {
        "release_date": "Saturday 02. January 1988", 
        "title": "Superman"
      }, 
      "27": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GCMail"
      }, 
      "28": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "CalCMail"
      }, 
      "29": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCMail"
      }, 
      "30": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "GelCCCMail"
      }, 
      "31": {
        "release_date": "Tuesday 08. June 1999", 
        "title": "Gelly"
      }
    }, 
    "success": true
  }}

  Trying to update movie not in database:

  $ curl -d '{"title":"Gel","release_date":"1999-06-08"}' -H "Content-Type: application/json" -X PATCH 127.0.0.1:5000/movies/32
  {
    "error": 404, 
    "message": "resource not found", 
    "success": false
  }
  
- Add a movie - actor combination to the database:
  $ curl -d '{"movie_id":"34","actor_id":"13"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/moviecast
  {
    "moviecast": [
      {
        "artist_id": 13, 
        "id": 13, 
        "movie_id": 34
      }
    ], 
    "success": true
  }

- Delete a MovieCast entry (combination of movie and actor):

  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape", 
        "actor_ids": [
          1, 
          2
        ], 
        "movie_id": 1
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman", 
        "actor_ids": [
          2
        ], 
        "movie_id": 4
      }, 
      {
        "Actors": "Ginger, Amitabh", 
        "Release Date": "Tuesday 08. June 1999", 
        "Title": "Jojo11", 
        "actor_ids": [
          13, 
          1
        ], 
        "movie_id": 34
      }
    ], 
    "success": true
  }
  $ curl -d '{"movie_id":34,"actor_id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:5000/moviecast
  {
    "success": true
  }

  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
  {
    "movie_actor_list": [
      {
        "Actors": "Amitabh, Aamir", 
        "Release Date": "Sunday 05. February 1978", 
        "Title": "Great Escape", 
        "actor_ids": [
          1, 
          2
        ], 
        "movie_id": 1
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman", 
        "actor_ids": [
          2
        ], 
        "movie_id": 4
      }, 
      {
        "Actors": "Amitabh", 
        "Release Date": "Tuesday 08. June 1999", 
        "Title": "Jojo11", 
        "actor_ids": [
          1
        ], 
        "movie_id": 34
      }
    ], 
    "success": true
  }

  Trying to delete an actor-movie combination that does not exist: 

  $ curl -d '{"movie_id":34,"actor_id":13}' -H "Content-Type: application/json" -X DELETE 127.0.0.1:5000/moviecast
  {
    "error": 404, 
    "message": "resource not found", 
    "success": false
  }

  

  **Error Conditions:**



Trying to delete an actor ID which does not exist:
$ curl http://127.0.0.1:5000/actors/8 -X DELETE
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}

curl -d '{"name":"Abhishek","age":"33", "gender":"Male"}' -H "Content-Type: application/json" -X POST 127.0.0.1:5000/post
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}



Adding permissions movicast add/insert: 

$ curl --request POST -d '{"actor_id":3, "movie_id":4}' -H "Content-Type: application/json" http://127.0.0.1:5000/moviecast -H "Authorization: Bearer ${EXEC_PRODUCER_TOKEN}"
{
  "moviecast": [
    {
      "artist_id": 3, 
      "id": 26, 
      "movie_id": 4
    }
  ], 
  "success": true
}



