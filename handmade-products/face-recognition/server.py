from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from app.controllers.person_controller import blueprint as person_blueprint

app = Flask(__name__)
app.register_blueprint(person_blueprint)

if __name__ == "__main__":
    app.run()