# ACEest DevOps CI/CD demo

This repo contains:
- A small Flask app (`app/`) — ACEest Fitness API
- Pytest tests in `tests/`
- Dockerfile, Jenkinsfile for CI pipeline
- Kubernetes manifests in `k8s/`
- SonarQube properties

## Local run
1. cd app
2. python3 -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. python app.py
5. POST /log, GET /summary, /health

## Tests
From repo root:
```
pip install -r app/requirements.txt
pytest -q
```

## Docker
Build:
```
docker build -t <REGISTRY>/aceest-fitness:dev .
docker push <REGISTRY>/aceest-fitness:dev
```

## Jenkins
- Configure credentials (dockerhub-creds) in Jenkins.
- Create pipeline job pointing at this repo and Jenkinsfile.

## Kubernetes
- Replace image references in `k8s/*.yaml` to your registry.
- Use `kubectl apply -f k8s/` to deploy.