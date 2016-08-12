import json
from population_estimator.loader.model import load

with open('data.txt') as data_file:
    data = json.load(data_file)

load(data)
