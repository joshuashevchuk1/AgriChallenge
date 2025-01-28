
import api.app as common_server

def run_flask_app():
     server = common_server.CommonApp("9020")
     server.run_server()

if __name__ == '__main__':
    run_flask_app()