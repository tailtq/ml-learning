from flask import Flask

from app.controllers.face_controller import blueprint as face_blueprint

app = Flask(__name__)
app.register_blueprint(face_blueprint)

if __name__ == "__main__":
    app.run()
