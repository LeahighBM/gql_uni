# gql-uni
A simple Django app using GraphQL for its backend API

## Running
### Locally 
You can run the djago server locally on your own machine. Make sure you install all the dependencies via `pip install -r requirements.txt`. Once all the dependencies are installed, you can run the server with `python manage.py runserver`. If everything worked well, you should be able to navigate to `http://127.0.0.1:8000/graphql` where there should be a graphql playground 

### Docker
If you don't want to run locally and would prefer to run as a docker container, a Dockerfile has been provided. Simply run `docker build -t gql-uni .` (don't forget the dot). Once the image is built, you can launch a container with the following: `docker run -d -p 8000:8000 gql-uni:latest`. The server should be running in a docker container and be accessible via localhost (127.0.0.1) port 8000 or on your local network (probably an address like 192.x.x.x or 172.x.x.x) also on port 8000

