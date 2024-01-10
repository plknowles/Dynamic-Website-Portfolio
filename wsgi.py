# Gunicorn serves the flask server by running server.py if this script is executed directly. Gunicorn WSGI UNIX server: BENOITC/Gunicorn: Gunicorn ‘Green unicorn’ is a WSGI HTTP server for UNIX, fast clients and sleepy applications., GitHub. Available at: https://github.com/benoitc/gunicorn
from server import server as application

if __name__ == "__main__":
    application.run()