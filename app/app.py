
from flask import Flask
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from db import cur
app = Flask(__name__)


@app.route('/')
def hi_there():
    data = cur.execute("SELECT * FROM *")
    try:
        app.logger.info("Connecting to the database", os.environ.get('POSTGRES_PORT'))
    except:
        app.logger.error("Unable to connect to the database",os.environ.get('POSTGRES_PORT'))
    return data

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)