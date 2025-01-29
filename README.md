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

## Deployement plan for ECS containers

TODO:

To deploy this to ECS

- Code should be refactored with a yaml based config system
- Code should have a gitactions