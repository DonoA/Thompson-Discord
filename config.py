import json

config = {}

with open('config.json') as conf:
    config = json.load(conf)
