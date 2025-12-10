# Backend Repository

Repository contenant les microservices backend FastAPI.

## Structure

```
backend/
├── Microservices/
│   ├── auth/          # Service d'authentification
│   ├── users/         # Service de gestion des utilisateurs
│   ├── items/         # Service de gestion des items
│   └── gateway/       # API Gateway
├── Jenkinsfile        # Pipeline CI/CD Jenkins
└── README.md
```

## Pipeline Jenkins

La pipeline Jenkins effectue les étapes suivantes :

1. **Checkout** : Récupération du code source
2. **Tests** : Exécution des tests unitaires
3. **Build Docker Images** : Construction des images Docker pour chaque microservice
4. **Push to Docker Hub** : Envoi des images vers Docker Hub (aminamr/*)
5. **Trigger Helm Deployment** : Déclenchement de la pipeline Helm pour déployer les services

## Variables d'environnement

- `DOCKER_REGISTRY` : docker.io
- `DOCKER_USERNAME` : aminamr
- `VERSION` : Numéro de build Jenkins
- `HELM_PIPELINE_JOB` : Nom du job Jenkins pour Helm
- `KUBERNETES_NAMESPACE` : Namespace Kubernetes (dev/prod)

## Images Docker

Les images sont taggées avec :
- Version : `aminamr/{service}:{BUILD_NUMBER}`
- Latest : `aminamr/{service}:latest`

Services :
- `aminamr/auth`
- `aminamr/users`
- `aminamr/items`
- `aminamr/gateway`

## Configuration Jenkins

Créer les credentials suivants dans Jenkins :
- **docker-hub-credentials** : Credentials Docker Hub (username/password)

