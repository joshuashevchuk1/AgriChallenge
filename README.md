# Agri Challenge

## Requirements

If doing local development, mongo is required

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

## Using the api

Once the application ingests all data the following data inspection endpoints are available

```commandline
/api/weather
```

```commandline
/api/weather/stats
```

### Example usage:

```commandline
curl -X GET "http://localhost:5000/api/weather/stats?station_name=Station_A&year=2025&skip=0&limit=10"
```

## Deployement plan for ECS containers

TODO:

To deploy this to ECS

- Should be refactored with a yaml based config system
- Should have a git actions for deploying via codebuild
- Should have an external mongodb database and not rely internally storing any data
- Should have secrets stored in parameter store