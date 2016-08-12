from SPARQLWrapper import SPARQLWrapper, JSON
from population_estimator.config.dbpedia import SPARQL_QUERY_ENDPOINT


def send_query(endpoint, query):
    endpoint = endpoint
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def parse_country(country, label, countries):
    if country not in countries:
        countries[country] = {
            'uri': country,
            'labels': [label]
        }
    else:
        if label not in countries[country]['labels']:
            countries[country]['labels'].append(label)


def parse_results(results, cities, countries):
    for row in results:
        if row['subject']['value'] not in cities:
            cities[row['subject']['value']] = {
                'labels': list(),
                'population': int(row['populationTotal']['value']),
                'area': float(row['areaTotal']['value']),
            }
            parse_country(row['country']['value'], row['clabels']['value'], countries)
            cities[row['subject']['value']]['country'] = countries[row['country']['value']]
        else:
            if row['labels']['value'] not in cities[row['subject']['value']]['labels']:
                cities[row['subject']['value']]['labels'].append(row['labels']['value'])
            parse_country(row['country']['value'], row['clabels']['value'], countries)


def get_cities(iterations, all=None):
    countries = dict()
    cities = dict()
    i = offset = 0
    results = list()
    if all:
        while results is not None:
            query = """
                SELECT * WHERE {
                        ?subject rdf:type <http://dbpedia.org/ontology/City>.
                        ?subject <http://dbpedia.org/ontology/populationTotal> ?populationTotal.
                        ?subject <http://dbpedia.org/ontology/areaTotal> ?areaTotal.
                        ?subject <http://dbpedia.org/ontology/country> ?country.
                        ?country rdfs:label ?clabels.
                        ?subject rdfs:label ?labels.
                } LIMIT 10000 OFFSET %d""" % offset
            results = send_query(SPARQL_QUERY_ENDPOINT, query)
            parse_results(results["results"]["bindings"], cities, countries)
            i += 1
            offset = i * 10000
    else:
        for i in xrange(iterations):
            query = """
                            SELECT * WHERE {
                                    ?subject rdf:type <http://dbpedia.org/ontology/City>.
                                    ?subject <http://dbpedia.org/ontology/populationTotal> ?populationTotal.
                                    ?subject <http://dbpedia.org/ontology/areaTotal> ?areaTotal.
                                    ?subject <http://dbpedia.org/ontology/country> ?country.
                                    ?country rdfs:label ?clabels.
                                    ?subject rdfs:label ?labels.
                            } LIMIT 10000 OFFSET %d""" % offset
            results = send_query(SPARQL_QUERY_ENDPOINT, query)
            parse_results(results["results"]["bindings"], cities, countries)
            offset = i * 10000
    return cities
