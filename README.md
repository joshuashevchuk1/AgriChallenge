# Agri Challenge

## Requirements

- python3.9+
- mongodb
- docker

## Setup

To build this application use the following commands

```commandline
docker-compose up --build
```

```commandline
docker-compose down
```

This will initialize a flask application using mongodb as a database.
Data is ingested at the application level.

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

## Deployement plan for ECS containers

TODO:

To deploy this to ECS

- Should be refactored with a yaml based config system
- Should have a git actions for deploying via codebuild
- Should have an external mongodb database and not rely internally storing any data
- Should have secrets stored in parameter store