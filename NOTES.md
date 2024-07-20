# SRE Challenge: Stef Timmermans
This file is effectively a second README that describes the modifications made on my fork of the repository.

Changes include modifications to the main app logic to make the application more secure and providing means of varied deployments.

<br>

# Managing Kubernetes Cluster
**Requires Docker Desktop and minikube.**

1. Start a local cluster: `minikube start`
2. Tell minicube to use the local Docker daemon (i.e., not to look for a remote registry): `eval $(minikube -p minikube docker-env)`
3. Change directory into the application: `cd app`
4. Build the Docker image without executing it: `docker-compose build`
5. Verify that the image "app-server" exists with `docker images`
5. Apply the configuration files using kubectl
  - `kubectl apply -f deployment.yaml`
  - `kubectl apply -f service.yaml`
6. Access the application: `minikube service server`
7. Close the tunnel with `Ctrl+C`
8. Stop the minikube cluster: `minikube stop`
9. To re-view, repeat from Step 1

<br>

# Running Docker Container in Isolation 
**Requires Docker Desktop.**

1. Change directory into the application: `cd app`
2. Execute command `docker compose up --build`
3. View application on `http://localhost:5001`
4. Stop gracefully with `Ctrl+C`

<br>

# Vulerabilities Found

### #1: Public secret string assignment in `application.py` for logging key.

*Moved string to `.env` in the root directory. File was already gitignore'd.*

### #2: SQL query in `application.py` for login returned all rows in the users table to the client.

*Modified logic to make a sanitized query on the connection where only the relevant row (or none) is accessible by the client-side code.*

<br>

# Software Used

- Docker Desktop
- minikube
- kubectl
- kompose

<br>

# Dependencies Added

Installed `python-dotenv` version `1.0.1` for dotenv.
