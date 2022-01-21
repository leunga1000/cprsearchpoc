## CPR Search App POC

We've used django to speed up the REST part of the API as this includes CRUD to some

We've used a SQLite db to implement the POC. Obviously a server would be more appropriate further down the road.

## Other things to explore with more time
- lemmatize (botswana's)
- Use FastAPI
- store documents as vectors
- use a database which supports vector search e.g.
- redis (new)
- elasticsearch (also ann)
- retrain a bert model or train a new model
- pagination on list and search results
- add some more tests
- improve reg exps for especially for numbers with punctuations.
- n-grams/sentences/docs as a whole?
- move to docker compose file to pull into db containers for local experiments
- run code formatter
- include title, sectors

## Installation instructions

on *nix: make a virtual environment, install pip requirements and 


```sh
python -m spacy download en_core_web_md
run.sh
```

OR

Docker, if you prefer docker or you are running on windows and spacy doesn't install.

In the directory with the Dockerfile:
```sh
docker build -t cpr . && docker run -p 8000:8000 cpr

# or with live reload (%cd% on windows instead of $PWD)
docker build -t cpr . && docker run -p 8000:8000 -v $PWD/cpr:/usr/src/app cpr
docker build -t cpr . && docker run -p 8000:8000 -v %cd%/cpr:/usr/src/app cpr
```
The endpoints will be accessible after seeing the message "Watching for file changes with StatReloader" or similar.


## Endpoints
### API Docs
Autogenerated
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/

Add &format=json if you just want to see data in the browser

### REST API
http://127.0.0.1:8000/policy/ 
(supports CRUD via GET POST PUT PATCH DELETE)

### Search API
http://127.0.0.1:8000/policy/search?q=space separated search string

### Spacy Search API
http://127.0.0.1:8000/policy/spacy_search/?q=policy%20export



## Tests
Run some tests
```sh
python manage.py test
```
