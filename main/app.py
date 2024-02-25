from flask import Flask
from auth import auth_blueprint
from ervaringsdeskundige import ervaringsdeskundige_blueprint



app = Flask(__name__)

app.secret_key = 'super secret key'
app.register_blueprint(auth_blueprint)
app.register_blueprint(ervaringsdeskundige_blueprint)





if __name__ == '__main__':
    app.run(debug=True)