"""Projet 

Déployer, à travers d'une API, un modèle entraîné de prédiction 
en utilisant la philosophie DevOps sur un fournisseur de services cloud.

Groupe 4"""

#import libraries
from flask import Flask, request, jsonify
import requests
import numpy as np
from sys import argv
import pickle

#creation de l'application Flask
app = Flask(__name__)
app.json.sort_keys = False

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
    predictions = pickled_model.predict(np.array([[sepalLength, petalLength, sepalWidth, petalWidth]]))
    
    response_data = {
        "sepalLength": sepalLength,
        "petalLength": petalLength,
        "sepalWidth": sepalWidth,
        "petalWidth": petalWidth,
        "predictedSpecies" : labels[predictions[0]]
    }

    return jsonify(response_data)

#exécuter l'application sur le port 8081
if __name__ == '__main__':
    app.run(debug=True, port=8081, host="0.0.0.0")