# Vulerabilities Found

*#1: Public secret string assignment in `application.py` for logging key.*

### Moved string to `.env` in the root directory. File was already gitignore'd.

---

*#2: SQL query in `application.py` for login returned all rows in the users table to the client.*

### Modified logic to make a sanitized query on the connection where only the relevant row (or none) accessible by the client-side code.

# More Dependencies

Installed `python-dotenv` version `1.0.1` for dotenv.
