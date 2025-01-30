# simple config file to store env variables
import os

if os.environ.get('HOST') is not None:
    host = os.environ['HOST']
else:
    host = "0.0.0.0"