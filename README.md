# Warpnet SRE Challenge: Stef Timmermans
This file outlines my changes to the directory. For the original documentation see `ORIGINAL_README.md`. 

Changes include the main app logic to make the application more secure and providing means of varied deployments.

<br>

# Managing Kubernetes Cluster
**Requires Docker Desktop and minikube**

1. Ensure the local Docker daemon is running
2. Start a local cluster: `minikube start`
3. Tell minikube to use the local Docker daemon (i.e., not to look for a remote registry): `eval $(minikube -p minikube docker-env)`
4. Change directory into the application: `cd app`
5. Build the Docker image without executing it: `docker-compose build`
6. Verify that the image "app-server" exists with `docker images`
7. Apply the configuration files using kubectl
    - `kubectl apply -f deployment.yaml`
    - `kubectl apply -f service.yaml`
8. Access the application: `minikube service server`
9. Close the tunnel with `Ctrl+C`
10. Stop the minikube cluster: `minikube stop`
11. To re-view, repeat from Step 1

<br>

# Running Docker Container in Isolation 
**Requires Docker Desktop**

1. Ensure the local Docker daemon is running
2. Change directory into the application: `cd app`
3. Execute command `docker compose up --build`
4. View application on `http://localhost:5001`
5. Stop gracefully with `Ctrl+C`

<br>

# Virtualization Process (Apple Silicon)

1. Install Ubuntu Server for target architecture: https://docs.getutm.app/guides/ubuntu/
2. Install and open UTM (FOSS for macOS with Apple Silicon support), and create new VM
3. Choose "Virtualize" from main menu (choose "Emulate" if wanting to use different architecture)
4. Choose "Linux" and attach downloaded Ubuntu image to "Boot ISO Image", leave rest default
5. Continue on with initialization and choose appropriate storage option (~16+ GB)
6. If on Apple Silicon installing for Virtualization with Ubuntu Server...
    - Under the Ubuntu VM options, go to configurations (top right) and move the VirtIO Drive to be above the USB Drive
    - After hitting Save, click on the CD/DVD dropdown and hit Clear, it should now display "(empty)"
    - For more information see this Issues thread: https://github.com/utmapp/UTM/discussions/3716
7. Hit the play button on the VM and follow instructions to set up Ubuntu installation (use OpenSSH)
8. Repeat Step 6 if still buggy... you should now see a login prompt
9. After verifying that the installation works, enter `shutdown now` to safely close the virtual machine if you wish
10. From this point forward, it is likely easiest to continue via SSH-ing into Ubuntu Server through a more modern terminal on your main machine (such as iTerm 2), which can be done through `ssh username@ip` so long as the target server is active
11. Install any dependencies (such as git and python3), generate an SSH key for GitHub if necessary, and clone the repository
12. If configured correctly, the Flask application should run via the Virtual Machine using similar commands to `ORIGINAL_README.md` and be accessible on the network, which are:
    1. `python3 -m venv venv` (Ubuntu forces virtual environments for safety)
    2. `source venv/bin/activate`
    3. `cd app`
    4. `pip install -r requirements.txt`
    5. `flask --app application run --host=0.0.0.0`
    6. `Ctrl+C` to return to the terminal
    7. `deactivate` to close the virtual environment

<br>

# Vulnerabilities Found

### #1: Public secret string assignment in `application.py` for logging key.

*Moved string to `.env` in app. File was already gitignore'd. `database.db` was also removed from the repository for vulnerability reasons.*

### #2: SQL query in `application.py` for login returned all rows in the users table to the client.

*Modified logic to make a sanitized query on the connection where only the relevant row (or none) is accessible by the client-side code.*

### #3: Database connection in `application.py` implicitly closed.

*Explicitly closed connection at the end of the authentication logic as to not rely on sqlite3's garbage collection process to minimize resource use.*

<br>

# Software Used

- Docker Desktop
- minikube
- kubectl
- kompose
- UTM

<br>

# Dependencies Added

- `python-dotenv` version `1.0.1` for dotenv
