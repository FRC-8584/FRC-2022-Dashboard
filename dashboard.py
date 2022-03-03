from flask import Flask, make_response, redirect, render_template, request, url_for, Request
from models import json, Key_Manger, touch
from secrets import token_urlsafe
from os.path import isfile

def deal_requeste(type_of: str, data: str | bytes, raw_requests: Request):
    print(f"Get Request Type:{type_of}")
    try:
        print(f"Data:{data.decode('utf-8')}")
    except:
        print(f"Data:{data}")
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
    elif type_of == "include":
        return render_template(json.loads(data).get("file_name"))
    elif type_of == "record":
        data_list = [splt for splt in data.decode("utf-8").split("\r\n")]
        return_data = {
            "auto-slide": False,
            "red-card": False
        }
        print(data_list)
        for i in range(int(len(data_list) / 4)):
            list_id = 4 * i
            key_pos = data_list[list_id + 1].find("name=\"") + 5
            key = data_list[list_id + 1][key_pos:][1:-1]
            value = data_list[list_id + 3]
            if value == "true":
                value = True
            return_data[key] = value
        save_data(return_data)
    elif type_of == "get_data":
        data: dict = json.loads(data)

        team: str = data.get("team")
        screen: str = data.get("screen")

        response = make_response()
        try:
            record_data: dict = json.load(f"data/{team}.json")[screen]
            RP_Score = 0
            Score = 0
            hang_score = 0

            auto_ball = int(record_data["auto-height"]) + int(record_data["auto-low"])
            manual_ball = int(record_data["manual-height"]) + int(record_data["manual-low"])

            if record_data["auto-slide"]:
                Score += 2
            Score += 4 * int(record_data["auto-height"])
            Score += 2 * int(record_data["auto-low"])
            Score += 2 * int(record_data["manual-height"])
            Score += 1 * int(record_data["manual-low"])
            Score += [0, 4, 6, 10, 15][int(record_data["manual-hang"])]
            hang_score += [0, 4, 6, 10, 15][int(record_data["manual-hang"])]
            hang_score += [0, 4, 6, 10, 15][int(record_data["manual-hang-1"])]
            hang_score += [0, 4, 6, 10, 15][int(record_data["manual-hang-2"])]
            if auto_ball >= 5:
                if auto_ball + manual_ball >= 18:
                    RP_Score += 1
            else:
                if auto_ball + manual_ball >= 20:
                    RP_Score += 1
            if hang_score >= 16:
                RP_Score += 1
            RP_Score += int(record_data["win"])
            record_data["RP_Score"] = RP_Score
            record_data["Score"] = Score
            response.set_data(json.dumps(record_data))
        except:
            response.set_data("{}")
        return response
    return ("", 204)

def save_data(data: dict):
    file_name = data.get("recorder-team")
    screen = data.get("recorder-screen")
    if not isfile(f"data/{file_name}.json"):
        touch(f"data/{file_name}.json", "{}")

    old_data: dict = json.load(f"data/{file_name}.json")
    old_data[screen] = data
    json.dump(f"data/{file_name}.json", old_data)

class Web_UI():
    app = Flask(__name__)

    def __init__(self) -> None:
        pass

    @app.route("/", methods=["GET", "POST"])
    def root():
        request_type = request.headers.get("Request-type")
        if request_type != None:
            return deal_requeste(request_type, request.get_data(), request)
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

    @app.route("/rule")
    def rule():
        if Key_Manger.check(request.cookies.get("key")):
            return render_template("rule.html")
        return redirect(url_for("login"))

    @app.route("/data")
    def data():
        if Key_Manger.check(request.cookies.get("key")):
            return render_template("data.html")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        Key_Manger.delete(request.cookies.get("key"))
        return redirect(url_for("root"))

    def run(self):
        self.app.run("0.0.0.0", port=80, debug=True, use_reloader=False)