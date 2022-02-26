from flask import Flask, make_response, redirect, render_template, request, url_for
from models import json

def deal_requeste(_type: str, _data):
    print(f'Get Request Type:{_type}')
    print(f'Data:{_data}')
    if _type == "login":
        _data = json.loads(_data)
        user_profile: dict = json.load("data/profile.json")
        _response = make_response()
        _response.set_data(json.dumps({"successed": False}))
        if (_data.get("account"), _data.get("password")) in user_profile.items():
            _response.set_cookie(key="name", value=_data.get("account"))
            _response.set_cookie(key="uuid", value=_data.get("password"))
            _response.set_data(json.dumps({"successed": True}))
        return _response
    if _type == 'include':
        return render_template(json.loads(_data).get('file_name'))

class Web_UI():
    app = Flask(__name__)

    def __init__(self) -> None:
        pass

    @app.route("/", methods=["GET", "POST"])
    def root():
        authorize = (request.cookies.get("name"), request.cookies.get("uuid"))
        user_profile: dict = json.load("data/profile.json")
        if request.headers.get('Request-type') != None:
            return deal_requeste(request.headers.get("Request-type"), request.get_data())
        if authorize not in user_profile.items():
            return redirect(url_for("login"))
        return redirect(url_for("home"))

    @app.route("/login")
    def login():
        authorize = (request.cookies.get("name"), request.cookies.get("uuid"))
        user_profile: dict = json.load("data/profile.json")
        if authorize in user_profile.items():
            return redirect(url_for("root"))
        return render_template("login.html")

    @app.route("/home")
    def home():
        authorize = (request.cookies.get("name"), request.cookies.get("uuid"))
        user_profile: dict = json.load("data/profile.json")
        if authorize not in user_profile.items():
            return redirect(url_for("login"))
        return render_template("home.html")

    def run(self):
        self.app.run("0.0.0.0", port=80, debug=True)

if __name__ == "__main__":
    web = Web_UI()
    web.run()