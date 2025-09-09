import os, json

def load_seed():
    here = os.path.dirname(__file__)
    with open(os.path.join(here, 'data', 'seed.json')) as f:
        return json.load(f)
