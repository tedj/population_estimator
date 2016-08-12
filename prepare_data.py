import json
from population_estimator.loader.dbpedia import get_cities


def export_cities():
    with open('data.txt', 'w') as outfile:
        # to get all the data, use get_cities(all=True)
        data = get_cities(10)
        json.dump(data, outfile)

export_cities()
