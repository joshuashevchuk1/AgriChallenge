# Agri Challenge

## Requirements

- python3.9+
- mongodb
- docker

## Development

If you have a local mongodb server you can run the application with the following command

```commandline
python3 src/run.py
```

You get a docker image for mongodb as 

```commandline
docker pull mongo
```

```commandline
docker run -d -p 27017:27017 --name agri-mongo
```

Make sure where you run the application the application and the wx data is defined

```commandline
DATA_PATH=<path to your wx data>
```

Other wise, to build this application with docker use the following commands

```commandline
docker-compose up --build
```

```commandline
docker-compose down
```

This build a build the flask application and mongodb into a docker compose suite called

```commandline
agrichallenge
```

Once ingestion finishes (~60 seconds) the application will be accessible at localhost.

## Using the api

Once the application ingests all data the following data inspection endpoints are available

```commandline
/api/weather
```

```commandline
/api/weather/stats
```

### Example usage:

for GET weather

```commandline
 curl -X GET "http://localhost:9020/api/weather?station_name=USC00129557&skip=0&limit=10" 
```

for GET weather stats

```commandline
curl -X GET "http://localhost:9020/api/weather/stats?station_name=USC00129557&year=1991&skip=0&limit=10"
```

Swagger documentation can be found at 

```commandline
http://localhost:9020/
```

## Deployement plan for ECS containers

TODO:

To deploy this to ECS

- Should be refactored with a yaml based config system
- Should have a git actions for deploying via codebuild
- Should have an external mongodb database and not rely on internally storing any data
- Should have secrets stored in parameter store