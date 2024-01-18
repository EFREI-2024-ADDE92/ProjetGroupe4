"""Projet 

Déployer, à travers d'une API, un modèle entraîné de prédiction 
en utilisant la philosophie DevOps sur un fournisseur de services cloud.

Groupe 4"""

#import libraries
from flask import Flask, request, jsonify, Response
import requests
import numpy as np
from sys import argv
import pickle
import prometheus_client 
from prometheus_client import Counter
import time


# Creation de l'application Flask
app = Flask(__name__)
app.json.sort_keys = False


graphs = {
    'request_operations_total': Counter('python_request_operations_total', 'The total number of processed requests'),
    'processing_time_seconds': prometheus_client.Summary('python_processing_time_seconds', 'Processing time of each prediction'),
    'iris_virginica_predictions_total': Counter('python_iris_virginica_predictions_total', 'The total number of Iris-virginica predictions'),
    'iris_setosa_predictions_total': Counter('python_iris_setosa_predictions_total', 'The total number of Iris-setosa predictions'),
    'iris_versicolor_predictions_total': Counter('python_iris_versicolor_predictions_total', 'The total number of Iris-versicolor predictions')

}

@app.route("/metrics")
def requests_count():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")



#pour indiquer à Flask, quelle URL et méthode doivent déclencher cette fonction
@app.route("/predict", methods=["GET"])
def result():

    labels = np.array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    #sepalLength, petalLength, sepalWidth, petalWidth récupérés 
    #à partir des variables d'URL 'sepL', 'petL', 'sepW', 'petW'
    sepalLength = float(request.args.get('sepL'))
    petalLength = float(request.args.get('petL'))
    sepalWidth = float(request.args.get('sepW'))
    petalWidth = float(request.args.get('petW'))

    pickled_model = pickle.load(open('iris_model.pkl', 'rb'))

    # Measure the processing time
    start_time = time.time()

    predictions = pickled_model.predict(np.array([[sepalLength, sepalWidth, petalLength, petalWidth]]))

    end_time = time.time()
    processing_time = end_time - start_time

    # Count the number of Iris-virginica predictions 
    predicted_species = labels[predictions[0]]
    graphs['iris_virginica_predictions_total'].inc() if predicted_species == 'Iris-virginica' else None

    # Count the number of Iris-setosa predictions 
    predicted_species = labels[predictions[0]]
    graphs['iris_setosa_predictions_total'].inc() if predicted_species == 'Iris-setosa' else None

    # Count the number of Iris-setosa predictions 
    predicted_species = labels[predictions[0]]
    graphs['iris_versicolor_predictions_total'].inc() if predicted_species == 'Iris-versicolor' else None

    
    response_data = {
        "sepalLength": sepalLength,
        "petalLength": petalLength,
        "sepalWidth": sepalWidth,
        "petalWidth": petalWidth,
        "predictedSpecies" : labels[predictions[0]]
    }

    # Increment the counters for each request and prediction
    graphs['request_operations_total'].inc()
    graphs['processing_time_seconds'].observe(processing_time)

    # Simulate some processing time
    time.sleep(0.600)

    return jsonify(response_data)

#exécuter l'application sur le port 8081
if __name__ == '__main__':
    app.run(debug=True, port=8081, host="0.0.0.0")
