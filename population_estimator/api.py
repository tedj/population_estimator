from flask import Flask, request, json

app = Flask(__name__)

@app.route('/api/estimator/population', methods=["POST"])
def population_estimator_api():
    params = request.json
    results = {}
    return json.dumps(results)

