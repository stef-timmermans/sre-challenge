# Running Dockerfile

1. Change directory into `app`
2. Excute command `docker compose up --build`
3. View application on `http://localhost:5001`
4. Close project gracefully with `Ctrl+C`

# Vulerabilities Found

### #1: Public secret string assignment in `application.py` for logging key.

*Moved string to `.env` in the root directory. File was already gitignore'd.*

### #2: SQL query in `application.py` for login returned all rows in the users table to the client.

*Modified logic to make a sanitized query on the connection where only the relevant row (or none) is accessible by the client-side code.*

<br>

# Dependencies Added on Fork

Installed `python-dotenv` version `1.0.1` for dotenv.

<br>

# Personal Notes

- I attempted to use the example Vagrant and Minikube software, but as I am developing on an Apple Silicon-based computer, I encountered spotty support and outdated dependencies for the ARM architecture. After trying Vagrant with VMware Fusion and VirtualBox, and facing persistent `vagrant up` errors despite extensive research on GitHub Issues, I opted for more widely supported software like Docker to set up the containerization process for the Kubernetes cluster. Note that I do have a Windows laptop, but it is much less powerful than my MacBook, and my workstation is configured around the latter's Thunderbolt 4 I/O.
