# ==========================================
# RMS System — app.py
# gawa ni [Your Name]
# Taglish comments para mas madali intindihin
# ==========================================

# import muna lahat ng kailangan nating modules
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, flash, send_from_directory
)
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from MySQLdb.cursors import DictCursor

# gumawa tayo ng flask app (parang main program)
app = Flask(__name__)
app.secret_key = "your_secret_key"  # pang-protect sa session data

# ===========================
# MySQL Database Settings
# (dito natin kinokonek yung app sa database)
# ===========================
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "zd552kl"
app.config["MYSQL_DB"] = "rms_db"
mysql = MySQL(app)

# ==========================================
# LOGIN PAGE — dito nag-lologin si user
# ==========================================
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # kunin yung inputs galing sa login form
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # i-check kung meron ba sa database
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        # kung meron, tsaka icheck kung tama password
        if user and check_password_hash(user["password"], password):
            # ilagay info sa session (para alam ni system na naka-login)
            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    # pag wala pang submit, ipakita lang yung login.html
    return render_template("login.html")

# ==========================================
# DASHBOARD — main page after login
# ==========================================
@app.route("/dashboard")
def dashboard():
    # kung walang naka-login, ibalik sa login page
    if "user_id" not in session:
        return redirect(url_for("login"))

    # kunin lahat ng users para ipakita sa table
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()

    # ipasa yung users list sa dashboard.html
    return render_template("dashboard.html", users=users)

# ==========================================
# ADD RECORD — pangdagdag ng new user
# ==========================================
@app.route("/add_record", methods=["POST"])
def add_record():
    # kunin lahat ng input galing form
    fullname = request.form["fullname"].strip()
    email = request.form["email"].strip()
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    role = request.form["user_role"]

    # validation muna bago mag-save
    if not fullname or not email or not username or not password:
        return jsonify({"status": "error", "message": "Please fill all fields."})

    # check kung may kapareho sa database
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
    existing = cur.fetchone()
    if existing:
        cur.close()
        return jsonify({"status": "error", "message": "Username or email already taken."})

    # hash muna yung password bago isave (for safety)
    hashed = generate_password_hash(password)

    # insert na sa database
    cur.execute(
        "INSERT INTO users (fullname, email, username, password, user_role) VALUES (%s, %s, %s, %s, %s)",
        (fullname, email, username, hashed, role)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "success", "message": "Record added successfully!"})

# ==========================================
# EDIT RECORD — pag may gusto kang baguhin
# ==========================================
@app.route("/edit_record/<int:user_id>", methods=["POST"])
def edit_record(user_id):
    # kunin bagong data sa form
    fullname = request.form["fullname"].strip()
    email = request.form["email"].strip()
    username = request.form["username"].strip()
    role = request.form["user_role"]

    if not fullname or not email or not username:
        return jsonify({"status": "error", "message": "Please fill all fields."})

    cur = mysql.connection.cursor(DictCursor)

    # check kung may kapareho (pero iba ang ID)
    cur.execute(
        "SELECT * FROM users WHERE (email=%s OR username=%s) AND id != %s",
        (email, username, user_id)
    )
    existing = cur.fetchone()

    if existing:
        cur.close()
        return jsonify({"status": "error", "message": "Username or email already taken."})

    # update na sa database
    cur.execute(
        "UPDATE users SET fullname=%s, email=%s, username=%s, user_role=%s WHERE id=%s",
        (fullname, email, username, role, user_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "success", "message": "Record updated successfully!"})

# ==========================================
# DELETE RECORD — tanggalin user
# ==========================================
@app.route("/delete_record/<int:user_id>", methods=["POST"])
def delete_record(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"status": "success", "message": "Record deleted successfully."})

# ==========================================
# LOGOUT — pang-alis ng session data
# ==========================================
@app.route("/logout", methods=["GET", "POST"])
def logout():
    # linisin muna lahat ng session (para mag-logout)
    user_id = session.get("user_id")
    session.clear()

    # optional: pang-debug lang to (makikita sa console)
    print(f"User {user_id} logged out successfully.")

    # balik sa login page
    return redirect(url_for("login"))

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js", mimetype="application/javascript")
# ==========================================
# Pang-run ng flask app
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)