from factoryworldwide_app.server import app
from factoryworldwide_app.controllers.WebController import web
from factoryworldwide_app.controllers.AuthController import auth

app.register_blueprint(web)
app.register_blueprint(auth)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True)
