from py2neo import Graph as neoGraph, Node, Relationship

neo_graph = neoGraph()


def attach_labels(node, labels):
    for label in labels:
        label_node = Node("Label", label=label)
        neo_graph.merge(label_node)
        node_has_label = Relationship(node, "HAS_LABEL", label_node)
        neo_graph.merge(node_has_label)


def load(data):
    for city in data:
        city_escape_quote = city.replace('"','\\"')
        merge_city_node_query = """
        MERGE (c:City {uri: "%s"})
        SET c = {uri: "%s", population: %d, area: %d}
        RETURN c
        """ % (city_escape_quote, city_escape_quote, data[city]['population'], data[city]['area'])
        cursor = neo_graph.run(merge_city_node_query)
        city_node = cursor.evaluate()
        if city_node is None:
            city_node = Node("City", uri=city, population=data[city]['population'], area=data[city]['area'])
        attach_labels(city_node, data[city]['labels'])
        country_node = Node("Country", uri=data[city]['country']['uri'])
        attach_labels(country_node, data[city]['country']['labels'])
        city_part_of_country = Relationship(city_node, "IS_PART_OF", country_node)
        neo_graph.merge(city_part_of_country)

