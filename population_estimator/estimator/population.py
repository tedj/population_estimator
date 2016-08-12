import math
from py2neo import Graph as neoGraph
neo_graph = neoGraph()


def population_density(population, area):
    if area == 0:
        return 0
    return float(population) / area


def circle_area(radius):
    return (1000 * radius) ** 2 * math.pi


def estimate_population(population, area, radius):
    if radius is None:
        return population
    density = population_density(population, area)
    selected_area = circle_area(radius)
    return int(density * selected_area)


def search(q, radius):
    query = """
        MATCH (cityLabel:Label)-[]-(city:City)-[]-(country:Country)
        WHERE cityLabel.label='%s'
        RETURN city, country
    """ % q
    items = list()
    cursor = neo_graph.run(query)
    for record in cursor:
        items.append({
            'uri': record['city']['uri'],
            'country': record['country']['uri'],
            'population_estimation': estimate_population(
                record['city']['population'],
                record['city']['area'],
                radius
            )
        })
    return items
