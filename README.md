# Description

This is a webservice that give an estimate about the population in a specific area.

# Data preparation

The data we use is from DBpedia knowledge base. We use SPARQL and dbpedia endpoint to query data about cities in the world with their totalpoulation and area.

We parse the data from rdf results and put it as a json file.
The JSON file contains a list of cities, each city has a uri identifier with a list of labels, the country with a list of lables, population size and the area.

# Data model
Once the data is prepared, we use neo4j graph database to represent our model.
Cities are stored in "City" nodes, each city node has a relation with a "Label" node to represent different names of the same city in different languages, since the user can invoke the webservice using queries in different languages.
The city node is also connected to the country node "Country", with "IS_PART_OF" relationship. This will be useful for filtering with countries, since we can find the same name of given city in different countries.

# How to the extend the data?
The population size changes periodically, and the data can be extended or updated. The model loader make sure to merge the data when it is needed.
# Population estimation
We estimate the population by calculating the population density first and we multiply it with the calculated circle area of the given radius.

# Limitations of the implementation:
- The data preparation time, it takes minutes to prepare the data from dbpedia knowledge base, however we can solve this issue by downloading dbpedia files locally, import them to fuseki jena to update the sparql endpoint in the config file, this should run the preparation script much faster.
- Tests: We should add some basic unit tests in the project.

# Requirements
The webservice is running with Flask and use the following libraries:
- py2neo
- SPARQLWrapper


The database is running with ne4oj graph database v > 3.0.

# Project Structure
The project has two main modules:
- The loader module which is responsible for extracting and parsing data from the knowledge base, and loading them to neo4j database.
- The estimator module which is responsible for searching for the requested place and computing the estimated population size.
# Run
- Preparing the data: We have a data.txt sample already prepared, to update this file with new cities, just run the following command
` python prepare_data.py `
- Loading the data: Make sure neo4j is running and then run the following command:
` python load_data.py `
- Starting the webservice:
` python run_web_service.py `

# Web Service parameters and output
##Request
###HTTP request
` POST /api/estimator/population `
###Parameters
Parameter name | Value	| Description
---------------| -------|------------
q | string | the place name e.g. Mumbai
radius | float | the radius in km e.g 30.0
##Response
If successful, this method returns a response body with the following structure:

`[
   {
     "country": "http://dbpedia.org/resource/India",
     "population_estimation": 58510742,
     "uri": "http://dbpedia.org/resource/Mumbai"
   }
 ]`
