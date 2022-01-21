## CPR Search App POC

We've used django to speed up the REST part of the API as this includes CRUD in some circles!

We've used a SQLite db to implement the POC. Obviously a server would be more appropriate further down the road.

Text is processed at db construction and dynamically when new documents are added. Punctuation is removed and text is lowercased. A terms column is added for simplyfying lookups.


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

### on *nix environments: 

#### Make a virtual environment, e.g. virtualenvwrapper
```sh
pip install virtualenvwrapper
mkvirtualenv cpr
```

#### Install Pip and requirements
```sh
pip install --upgrade pip
pip install -r requirements.txt
```


#### Optional: Download spacy data file
```sh
python -m spacy download en_core_web_md
run.sh
```

OR

### Docker, if you prefer docker or you are running on windows and spacy doesn't install.

#### Starting Docker
In the directory with the Dockerfile:
```sh
docker build -t cpr . && docker run -p 8000:8000 cpr

# or with live reload (%cd% on windows instead of $PWD)
docker build -t cpr . && docker run -p 8000:8000 -v $PWD/cpr:/usr/src/app cpr
docker build -t cpr . && docker run -p 8000:8000 -v %cd%/cpr:/usr/src/app cpr
```
The endpoints will be accessible after seeing the message "Watching for file changes with StatReloader" or similar.

#### Stopping Docker
```sh
docker ps
docker stop *dockerid*
```
Just the first few letters of the docker id will do.


## Endpoints

Once you have the server running in the terminal with the message "Watching for file changes with StatReloader" or similar, one can access the endpoints with a browser or favoured http client, e.g. wget, curl, python requests, httpie

### API Docs
Autogenerated
<http://127.0.0.1:8000/swagger/>

<http://127.0.0.1:8000/redoc/>

### REST API
For the following endpoints,
Add &format=json if you just want to see data in the browser, otherwise you will see the Django Rest Framework colours and formatting.

Policy objects: list for all, or supply an id to interact with a policy by id

<http://127.0.0.1:8000/policy/>

<http://127.0.0.1:8000/policy/10088/>
(supports CRUD ops via GET POST PUT PATCH DELETE)

### Search API

Search using Jaccard Similarity, the size of the intersection of the size of the union of two documents.

<http://127.0.0.1:8000/policy/search?q=space separated search string>


### Spacy Search API
Search using Spacy's simliarity functionality, spacy_similarity score included.
<http://127.0.0.1:8000/policy/spacy_search/?q=policy%20export>




## Tests
Run tests
```sh
python manage.py test
```
