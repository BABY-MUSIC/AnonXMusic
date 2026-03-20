import json
import os

lang = {}

p = os.path.dirname(__file__)

f = os.path.join(p, "en.json")

if os.path.exists(f):
    lang = json.load(open(f, encoding="utf-8"))


# =========================
# GET STRING
# =========================

def get_string(key):

    return lang.get(key, key)
