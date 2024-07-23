import sqlite3
import logging
from flask import Flask, session, redirect, url_for, request, render_template, abort

# For .env files in Python
# https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

"""
VULNERABILITY #1
Type: Secrets
Description:
    Secret string (for logging) public in repository.
Prevention:
    Easiest way is to store this key in a file not included in the
    repo. This file would need to be added to the .gitignore before
    any further commits are made (though this is already the case).
    This method still has a relatively high potential of user error
    in handling the .env file, so production applications that may
    be attacked should follow more modern and robust solutions than
    this one.
"""
app.secret_key = os.getenv("LOG_KEY")
app.logger.setLevel(logging.INFO)

# Use relocated .db file
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def is_authenticated():
    if "username" in session:
        return True
    return False


def authenticate(username, password):
    connection = get_db_connection()

    """
    VULNERABILITY #2
    Type: Credentials in Client
    Description:
        Due to the `SELECT * FROM users`, all rows from the users table
        is loaded onto the client side, which eliminates the security from
        the (hopefully) secure external database. Although third-party
        authentification is becoming more and more standard with many companies
        forgoing any risk of dealing with credentials, this authenticate function
        will maintain its intended behavior.

        This code makes the assumption that usernames are unique. The username
        and password also need to be sanitized to prevent SQL Injection in this case,
        as we are passing user data into the query.
        Real Python's article on preventing injection attacks:
        https://realpython.com/prevent-python-sql-injection/
        About sqlite3 cursor:
        https://www.tutorialspoint.com/python_data_access/python_sqlite_cursor_object.htm

        Logging passwords is inherently unsafe, as it creates a physical liability, so
        that element of the logic was removed.
    """

    # Use sqlite3's cursor object to determine whether a username/password was valid
    cursor = connection.cursor()
    
    # Use sanitized query, treating username and passwords as strings, not queries
    # Do filter on the database side, not the client
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    
    """
    VULNERABILITY #3
    Type: Database Connection Not Released
    Description:
        Though more a practical vulnerability than a security one, the original
        code did not close the database connection ("database.db") at the end
        of the authentication logic. It is best practice to close a connection
        when no longer in use rather than rely on sqlite3's automatic garbage
        collector (i.e., the connection going out of scope at the end of this
        function where it was created).

        Keeping a connection open does not directly correlate to security issues, but
        can lead to problems in terms of scalability and resource management. See:
        https://stackoverflow.com/questions/312702/is-it-safe-to-keep-database-connections-open-for-long-time
        https://www.reddit.com/r/learnpython/comments/ystjwc/database_connection_should_it_be_kept_open/
    """
    # Check if the query result was empty/truthy
    result = cursor.fetchone()
    if result:
        # If result exists, use same logic as before in setting session state
        # Removed logging of password
        app.logger.info(f"the user '{username}' logged in successfully")
        session["username"] = username

        # Close the connection
        connection.close()

        # Signal to caller that user has logged in
        return True
    else:
        # Otherwise, log the attempt and return code 401: Unauthorized

        # Removed logging of password
        app.logger.warning(f"the user '{ username }' failed to log in")

        # Close the connection
        connection.close()

        # Signal HTTP 401: Unauthorized
        abort(401)


@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
