# Applications of Big Data  - Projet 

## Groupe 4 :

#### Frimpong ADOTRI
#### Suvéta ANANDARAJ
#### Abisha JEYAVEL 
#### Thushanthy THEIVENDIRAN
#### Augusta Merveille TSAMPI MEZAGUE 


---

<img src="https://miro.medium.com/v2/resize:fit:1400/1*_sPi4LqKsepotYHWlH_32g.png" width=800>

<img src="https://miro.medium.com/v2/resize:fit:1400/1*zqMeeKJJNGqbXr8WBKzdFw.png" width=800>

---
## 1. Objectif du projet : 
---

Déployer, à travers d'une API, un modèle entraîné de prédiction en utilisant la philosophie
DevOps sur un fournisseur de services cloud.

<br/>

---
## 2. Entrainement d'un modèle de KNN sur le dataset iris
---

<br/>

---
## 3. Code Python modelApi.py
---

Le but de ce script est de développer un serveur web utilisant Flask. Ce serveur a pour but de déployer le modèle de prédiction de classification d'espèces d'Iris via une API REST. 

Le code intègre aussi des métriques de suivi, utilisant Prometheus pour mesurer les statistiques liées aux prédictions et aux performances du serveur. 

Voici les métriques Prometheus définis : 

- **python_request_operations_total** : Le nombre total de requetes traitées
- **python_processing_time_seconds** : Temps de traitement de chaque prédiction
- **python_iris_virginica_predictions_total** : Le nombre total de prédictions Iris-virginica
- **python_iris_setosa_predictions_total** : Le nombre total de prédictions Iris-setosa
- **python_iris_versicolor_predictions_total** : Le nombre total de prédictions Iris-versicolor

<br/>

Dans ce script, on définit deux endpoints : 

- ```/predict``` pour effectuer des prédictions en utilisant le modèle entrainé dans le notebook **model_training.ipynb**s
- ```/metrics``` pour exposer les métriques Prometheus. Il renvoie les métriques au format texte/plain. 

<br/>

---
## 4. Dockerfile : Fichier de configuration 
---

Dockerfile permet de configurer et créer rapidement une image Docker. Dans le Dockerfile, on écrit les instructions décrivant les actions que l’image Docker doit exécuter une fois qu’elle sera créée.

Voici les instructions pour notre image Docker :


```bash
FROM python:3.11-slim-bookworm
```
- Notre image Docker va être créée à partir de l'image de ```python:3.11-slim-bookworm```   

<br/>

```bash
WORKDIR /app
```
- On définit le dossier de travail pour les autres commandes comme RUN, CMD.

<br/>

```bash
COPY iris_model.pkl /app
COPY modelApi.py /app
COPY requirements.txt /app
```
- On copie le fichier **iris_model.pkl**, **modelApi.py** et **requirements.txt** dans le conteneur Docker à partir de notre machine. 

<br/>

```bash
RUN pip install --no-cache-dir --requirement requirements.txt
```
- On lance la commande pour installer les librairies définis dans le **requirements.txt**. 

<br/>

```bash
CMD ["python", "modelApi.py"]
```
- La commande **CMD​** spécifie l'instruction qui doit être exécutée au démarrage du conteneur Docker. On exécute la commande ```python modelApi.py``` en mode shell. 

<br/>

---
## 5. Configuration de Github Action
---

Dans ```.github/workflows```, on crée le fichier de workflow ```docker-image.yml```. 


```bash
on:
  push:
    branches:
      - main
```
- Le workflow s'exécute quand on fait un ```push``` sur la branche ```main``` du dépôt Github. 

<br/>

- Dans ```jobs```, on regroupe toutes les jobs, qui doivent être exécutées dans notre workflow. 

- Dans ```steps```, on définit les étapes de notre workflow : 
    - 1ère étape : ```Checkout GitHub Action``` : En utilisant l'action **actions/checkout@main**, on récupére notre code source 
   
    ```bash
    name: 'Checkout GitHub Action'
    uses: actions/checkout@main
    ```

    - 2ème étape : ```Hadolint for check the code``` : En utilisant l'action **hadolint/hadolint-action@v3.1.0**, on vérifie la conformité du **Dockerfile** avec les pratiques définies par Hadolint
   
    ```bash
    name: 'Hadolint for check the code' 
    uses: hadolint/hadolint-action@v3.1.0
    with:
        dockerfile: ./Dockerfile 
    ```

    - 3ème étape : ```Login via Azure CLI``` : Avec l'action **azure/login@v1**, on se connecte à Azure CLI en utilisant la variable AZURE_CREDENTIALS stockée dans les secrets GitHub.
   
    ```bash
    name: 'Login via Azure CLI'
    uses: azure/login@v1
    with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
        version: '2022-11-01-preview'
    ```

    - 4ème étape : ```Create Container App Environment``` : En utilisant la commande Azure CLI, on crée un environnement d'application conteneurisée avec des paramètres tels que le groupe de ressources, le nom, et l'emplacement.
   
    ```bash
    name: 'Create Container App Environment'
    run: |
    az containerapp env create \
        -g ${{ secrets.RESOURCE_GROUP }} \
        -n groupe4containerapp-bis \
        --location 'france central'
    ```

    - 5ème étape : ```Build and push image``` : Avec l'action **azure/login@v1**, on se connecte au registre Docker sur Azure avec les informations d'identification stockées dans les secrets GitHub. Puis, on construit l'image Docker à partir du **Dockerfile** avec la commande ```docker build```. Puis, on publie l'image Docker dans le registre Azure avec la commande ```docker push```.
   
    ```bash
    name: 'Build and push image'
    uses: azure/docker-login@v1
    with:
        login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    run: |
        docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/projetirisgroupe4:${{ github.sha }}
        docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/projetirisgroupe4:${{ github.sha }}
    ```

    - 6ème étape : ```Build and deploy Container App``` : En utilisant l'action **azure/container-apps-deploy-action@v1**, on déploie l'application conteneurisée sur Azure Container Apps. 
   
    ```bash
    name: Build and deploy Container App
    uses: azure/container-apps-deploy-action@v1
    with:
        acrName: efreibigdata           
        containerAppName: groupe4containerapp
        containerAppEnvironment : groupe4containerapp-bis
        resourceGroup: ${{ secrets.RESOURCE_GROUP }}
        imageToDeploy: ${{ secrets.REGISTRY_LOGIN_SERVER }}/projetirisgroupe4:${{ github.sha }}
        location: 'france central'
        targetPort: 8081
        registryUsername: ${{ secrets.REGISTRY_USERNAME }}
        registryPassword: ${{ secrets.REGISTRY_PASSWORD }}
        acrUsername: ${{ secrets.REGISTRY_USERNAME }}
        acrPassword: ${{ secrets.REGISTRY_PASSWORD }}
        azureCredentials : ${{ secrets.AZURE_CREDENTIALS }}
    ```

    - 7ème étape : ```Configure autoscaling``` : En utilisant la commande Azure CLI, on configure l'autoscaling de l'application conteneurisée. Cette règle d'autoscaling est basée sur la concurrence HTTP.
   
    ```bash
    name: 'Create Container App Environment'
    run: |
    az containerapp env create \
        -g ${{ secrets.RESOURCE_GROUP }} \
        -n groupe4containerapp-bis \
        --location 'france central'
    ```

<br/>

---
## 6. Test de charge avec Locust
---

<br/>

---
## 7. Configuration de docker-compose.yaml
---

<br/>

---
## 8. Configuration de prometheus.yaml
---

```bash
global:
  scrape_interval: 15s
  scrape_timeout: 10s

scrape_configs:
  - job_name: 'services'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['prometheus:9090', 'iris-api:8081']
```

Ce fichier de configuration de Prometheus est utilisé pour scrapper les métriques à partir de differents services. Il scrape toutes les 15 secondes. On a définit un délai d'attente de 10 secondes. Si le scrapping prend plus de 10 secondes , elle sera interrompue. 

<br/>

---
## 8. Test
---

<br/>

---
## 9. Partie Bonus
---

- Utilisation d'un linter pour Dockerfile dans la pipeline de déploiement pour s'assurer de sa
cohérence.

    À l'exécution de la commande suivante, on a 0 lint erreurs sur notre Dockerfile. 

```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

- Ajout d'un endpoint ```/metrics``` en utilisant la bibliothèque prometheus-client , exposant 5 métriques Prometheus définis. 

- Branchement de Prometheus à Grafana