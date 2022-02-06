# Library API - a dockerized FastAPI sample project 📖

The following is a test project that uses FastAPI and SQLAlchemy to develop a backend for a fictional library website. 

It is used as a sample repository for this [Docker tutorial](https://luisgc93.medium.com/docker-for-newbies-24601dfd1e6c) and is also deployed on heroku at: https://book-api-fastapi-project.herokuapp.com/.

## Usage
Start the project containers with the `make start` command. 

Access the project's health endpoint to check that everything is running correctly:
http://0.0.0.0:8000/docs

You can then check the full API spec can be found at:
http://0.0.0.0:8000/docs


Example request to POST /books:
````
curl --location --request POST '0.0.0.0:8000/books/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Harry Potter and the Philosopher'\''s Stone",
    "author": "J. K. Rowling"
}'
````
