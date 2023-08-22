
from flask import Flask
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
secret = os.environ.get('POSTGRES_DB')
print(secret)
app = Flask(__name__)


@app.route('/')
def hi_there():
    return 'Start Api'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)