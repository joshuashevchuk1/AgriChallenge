# simple config file to store env variables
import os

# app envs

if os.environ.get('HOST') is not None:
    HOST = os.environ['HOST']
else:
    HOST = "0.0.0.0"

if os.environ.get('PORT') is not None:
    PORT = os.environ['PORT']
else:
    PORT = 9020

if os.environ.get('DATA_PATH') is not None:
    DATA_PATH = os.environ['DATA_PATH']
else:
    DATA_PATH = "./src/app/data/wx_data"

# mongo envs

if os.environ.get('MONGO_HOST') is not None:
    MONGO_HOST = os.environ['MONGO_HOST']
else:
    MONGO_HOST = "localhost"

if os.environ.get('MONGO_PORT') is not None:
    MONGO_PORT = os.environ['MONGO_PORT']
else:
    MONGO_PORT =  27017

if os.environ.get('MONGO_USER') is not None:
    MONGO_USER = os.environ['MONGO_USER']
else:
    MONGO_USER = None

if os.environ.get('MONGO_PASS') is not None:
    MONGO_PASS = os.environ['MONGO_PASS']
else:
    MONGO_PASS = None
