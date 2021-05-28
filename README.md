# [DEMO](https://secret-anchorage-17084.herokuapp.com)

# CustomersBackend


## Run locally

(run this commands after clonning the repository)

`$ pip install requirements.txt`

`$ cd app`

`$ uvicorn main:app --reload`


## Test

`$ pip install pytest`


`$ pytest`

## Production

On production, the code uses the official image uvicorn-gunicorn-fastapi:latest (see Dockerfile) to serve the app on heroku, with guinicorn managind uvicorn instances for asyncronous requests.

### Commands

`$ docker build -f Dockerfile -t fastapiimage ./`

`$ heroku container:push web --app secret-anchorage-17084`

`$ heroku container:release web --app secret-anchorage-17084`

