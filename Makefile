build:
    docker build -t skin_disease_pred_api:v1 .
run:
    docker run -d -p 8000:8000 --name skin_disease_pred_api skin_disease_pred_api:v1
remove:
    docker rm -f skin_disease_pred_api
rebuild:
    docker build -t skin_disease_pred_api:v1 .
    docker rm -f skin_disease_pred_api
    docker run -d -p 8000:8000 --name skin_disease_pred_api skin_disease_pred_api:v1