from flask import Flask, make_response, redirect, render_template, request, url_for
from models import json, Key_Manger
from secrets import token_urlsafe

def deal_requeste(type_of: str, data: str):
    print(f'Get Request Type:{type_of}')
    print(f'Data:{data}')
    if type_of == "login":
        data: dict = json.loads(data)
        user_profile: dict = json.load("data/profile.json")

        account: str = data.get("account")
        password: str = data.get("password")

        response = make_response()
        response.set_data(json.dumps({"successed": False}))
        if (account, password) in user_profile.items():
            _login_key = token_urlsafe()
            Key_Manger.add(_login_key, account)

            response.set_cookie(key="key", value=_login_key)
            response.set_data(json.dumps({"successed": True}))
        return response
    if type_of == 'include':
        return render_template(json.loads(data).get('file_name'))

class Web_UI():
    app = Flask(__name__)

    def __init__(self) -> None:
        pass

    @app.route("/", methods=["GET", "POST"])
    def root():
        request_type = request.headers.get('Request-type')
        if request_type != None:
            return deal_requeste(request_type, request.get_data())
        if Key_Manger.check(request.cookies.get("key")):
            return redirect(url_for("home"))
        return redirect(url_for("login"))

    @app.route("/login")
    def login():
        if Key_Manger.check(request.cookies.get("key")):
            return redirect(url_for("root"))
        return render_template("login.html")

    @app.route("/home")
    def home():
        if Key_Manger.check(request.cookies.get("key")):
            return render_template("home.html")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        Key_Manger.delete(request.cookies.get("key"))
        return redirect(url_for("root"))

    def run(self):
        self.app.run("0.0.0.0", port=80, debug=True, use_reloader=False)