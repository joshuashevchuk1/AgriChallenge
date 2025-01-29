
import app.api as weather_api
import logging

logging.basicConfig(
        format='%(levelname)s*%(filename)s:%(lineno)d:  %(message)s'
    )
logging.root.setLevel(logging.INFO)

def run_flask_app():
     server = weather_api.WeatherApp("9020")
     server.initialize_database()
     #server.ingest() # comment this line out if you don't want to re-run the ingestion process
     server.run_server()

if __name__ == '__main__':
    run_flask_app()