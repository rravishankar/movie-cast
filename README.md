# **Movies and More :)**

The idea behind this application is helping the movie industry folks - casting assistants, casting directors and executive producers to manage their database of actors and movies. It includes the following for actors & movies:

- Getting a list 
- Adding 
- Deleting
- Updating
- Making a combination of actors and movies we call it "Moviecast". These Moviecasts  are open for viewing for everyone (need no authorization for viewing a Moviecast, but needs certain privileges for making such a combination).

The following sections describe the roles, the associated permissions/privileges and the details of the API's & later also have a note regarding the environment variables, testing the app locally & remotely on Heroku. The application uses Auth0 based authentication. The following sections are mainly for developers to understand the usage of the API



#### Permissions and Roles

With ref to the actors and movies we have the following permissions which are self explanatory 


###### List of Permissions

get:actors > Gets a list of actors (supports pagination)

post:actors > Add an actor

delete:actors > Delete an actor

update:actors > Update an actor's profile/detail

get:movies > Get a list of movies (supports pagination)

post:movies > Add a movie

delete:movies > Delete a movie

update:movies > Update a movie profile/detail


The following permissions are for adding/deleting  a combination of movie and actors

post:moviecast > Adding a combination of movie and actor

delete:moviecast > Deleting the movie-actor combination (Deleting a movie or an actor also deletes the moviecast associated with the movie or an actor)

One can get a list of current movie-cast combinations too. There is no authentication/permission required for getting a list of movie-cast combination.

###### Roles and permissions:

Every roles has been assigned a set of permissions based on their profile. The permission set is as below.

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



#### API Requests and Responses

The API  requests and respective JSON responses are listed out below for all the actions that can be pursued. 

The endpoint for the Heroku hosted API is  https://movie-dig.herokuapp.com/moviecast  and the API works only when appended with appropriate resource names and arguments.

GET requests are paginated with a page size of 5, eventually this API may be enhanced with support to modify the page size within reasonable limits.

Please note that all requests (except for moviecast GET requests) need to be added authentication header - the examples below DO NOT ADD THE AUTHENTICATION HEADER for reasons of brevity. The actual request would do something on the following lines (dummy Linux command prompt entries below):

e.g. : 

This sample example adds a combination of a movie and an actor to the system's database.

---Start of sample request and response---

For trying out on Heroku

$ curl --request POST -d '{"actor_id":3, "movie_id":4}' -H "Content-Type: application/json" https://movie-dig.herokuapp.com/moviecast -H "Authorization: Bearer <JWT token here>"

OR 

For trying out on localhost

$ curl --request POST -d '{"actor_id":3, "movie_id":4}' -H "Content-Type: application/json" http://127.0.0.1:5000/moviecast -H "Authorization: Bearer <JWT token here>"

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



The part in the command *--H "Authorization: Bearer <JWT token here>"* needs to be appended to each of the commands as required with the appropriate token which has the permission to carry out the activities for that role. Also if you are using the Heroku endpoint you need to substitute "http://127.0.0.1:5000/" in the examples below with  "https://movie-dig.herokuapp.com/"



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
  
- Add an actor

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

  

- Update actor details

  $ curl --request GET 'http://127.0.0.1:5000/actors'

  ID is before actor details
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

  

- Delete Actor : See example later in this documentation which also demonstrates the effect of the same on moviecast as well 

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

Support for pagination for movies:

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

- Get moviecasts or movies with details of cast, actors, release date
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
  
- Delete a Movie:

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

  Effect of delete movie on moviecast (see Moviecast in later sections):

  

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

  Add a movie - actor pair (for how to add an actor see documentation above)

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

- Update a Movie: $ curl --request GET 'http://127.0.0.1:5000/movies'
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
  
- Get a Moviecast & Delete actor with deletion of corresponding items in moviecast table:
  Request-response:
  
  $ curl --request GET 'http://127.0.0.1:5000/moviecast'
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
  
  "8": {
        "age": 33, 
        "gender": "Male", 
        "name": "Abhishek"
      }  
  
  }, 
    "success": true
  }
  
  Delete actor request and response:
  $ curl http://127.0.0.1:5000/actors/8 -X DELETE
  {
    "success": true
  }
  
  Post delete status of actors and moviecast table:
  
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
  
  
  
- Add a moviecast : movie - actor combination to the database:
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
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
      }, 
      {
        "Actors": "Ginger, Amitabh", 
        "Release Date": "Tuesday 08. June 1999", 
        "Title": "Jojo11"
  
  ​    }
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
        "Title": "Great Escape"
      }, 
      {
        "Actors": "Aamir", 
        "Release Date": "Saturday 02. January 1988", 
        "Title": "Superman"
    {
        "Actors": "Amitabh", 
        "Release Date": "Tuesday 08. June 1999", 
        "Title": "Jojo11"
  
  ​    }
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

Most error conditions are already covered above, here are a few more:

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



#### Notes for running the app locally

The file setup.sh mainly contains values like Auth0 parameters, JWT keys, logging level, deployment mode (DEPLOY_MODE) which decides whether the app runs in dev mode (local postgres database) OR uses the remote Heroku database among others.



### Tests

The tests to make sure everything is in order are in the files test_movies.py (for locally hosted setup) & test_movies_heroku.py (for Heroku hosted setup) 

