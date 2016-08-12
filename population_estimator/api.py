from flask import Flask, request, json
from population_estimator.estimator.population import search

app = Flask(__name__)


@app.route('/api/estimator/population', methods=["POST"])
def population_estimator_api():
    params = request.json
    radius = None
    if 'radius' in params:
        radius = params['radius']
    results = search(params['q'], radius)
    return json.dumps(results)

