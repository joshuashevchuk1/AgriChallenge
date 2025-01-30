# simple config file to store env variables
import os

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