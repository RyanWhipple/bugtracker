from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import thoughts
from flask_app.controllers import bugs

if __name__ == "__main__":
    app.run(debug=True)