import secrets
import person_controller
from logging import debug
from flask import Flask

# needs to have the secret key to work
secret = secrets.token_urlsafe(32)

# creates the flask app and connects via blueprint and runs the app on localhost:3000
app = Flask(__name__)
app.secret_key = secret
app.register_blueprint(person_controller.person_page)
app.run(debug=True, host="127.0.0.1", port="3000")
