from dashboard import Web_UI
from models import touch, Thread, json
from os.path import isfile
from os import system
from time import sleep
from subprocess import Popen, PIPE
import requests

def flask_job():
    web = Web_UI()
    web.run()

def check_update() -> bool:
    remote_id = json.loads(requests.get("https://api.github.com/repos/FRC-8584/FRC-2022-Dashboard/commits").content)[0]["sha"]
    git_id = str(Popen("git rev-parse HEAD", shell=True, stdout=PIPE).stdout.read())
    if remote_id not in git_id:
        Popen("git stash", shell=True, stdout=PIPE).stdout.read()
        Popen("git pull", shell=True, stdout=PIPE).stdout.read()
        return True
    return False

if __name__ == "__main__":
    if not isfile("data/key.json"):
        touch("data/key.json", "{}")

    flask_thread = Thread(target=flask_job)
    flask_thread.start()

    # while True:
    #     if check_update():
    #         flask_thread.stop()
    #         flask_thread.join()
    #         system("start cmd /c Start.cmd")
    #         exit()
    #     sleep(10)