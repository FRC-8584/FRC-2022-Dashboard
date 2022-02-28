from dashboard import Web_UI
from models import touch
from os.path import isfile

if __name__ == "__main__":
    if not isfile("data/key.json"):
        touch("data/key.json", {})

    web = Web_UI()
    web.run()