
import app.app as common_server
import logging

logging.basicConfig(
        format='%(levelname)s*%(filename)s:%(lineno)d:  %(message)s'
    )
logging.root.setLevel(logging.INFO)

def run_flask_app():
     server = common_server.CommonApp("9020")
     server.init_app()
     server.run_server()

if __name__ == '__main__':
    run_flask_app()