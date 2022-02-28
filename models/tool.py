from models import json

def touch(name: str, content: bytes | str = ""):
    if type(content) == str:
        content = bytes(content, "utf-8")
    with open(name, mode="wb") as touch_file:
        touch_file.write(content)
        touch_file.close()

class Key_Manger:
    def check(key: str) -> bool | str:
        key_data: dict = json.load("data/key.json")
        if key in key_data.keys():
            return key_data.get(key)
        else:
             return False

    def add(key: str, name: str):
        key_data: dict = json.load("data/key.json")
        key_data[key] = name
        json.dump("data/key.json", key_data)

    def delete(key: str):
        if Key_Manger.check(key):
            key_data: dict = json.load("data/key.json")
            del key_data[key]
            json.dump("data/key.json", key_data)