# simple config file to store env variables
import os

if os.environ.get('HOST') is not None:
    host = os.environ['HOST']
else:
    host = "0.0.0.0"

if os.environ.get('PORT') is not None:
    port = os.environ['PORT']
else:
    port = 9020

if os.environ.get('DATA_PATH') is not None:
    data_path = os.environ['DATA_PATH']
else:
    data_path = "./src/app/data/wx_data"