import sys
sys.path.insert(0, '/var/www/app/')

from flask import Flask

app = Flask(__name__)

from OS.views import *

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)

app.secret_key="Password"
