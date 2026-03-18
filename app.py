from flask import Flask, render_template, request, redirect

import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)

app.secret_key = "supersecretkey123"

@app.route("/init-db")
def init_db():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        approved INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        lat TEXT,
        lng TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        vaccinated TEXT,
        status TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adoptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        dog_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

    return "Database initialized!"



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/adopt")
def adopt():
    return render_template("adopt.html")


@app.route("/report", methods=["GET","POST"])
def report():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        location = request.form["location"]
        description = request.form["description"]

        print(name, phone, location, description)

        return redirect("/")

    return render_template("report.html")


@app.route("/volunteer", methods=["GET","POST"])
def volunteer():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        skills = request.form.get("skills")

        if not name or not email or not phone or not skills:
            return "Please fill all fields"

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO volunteers (name, email, phone, skills)
        VALUES (?, ?, ?, ?)
        """, (name, email, phone, skills))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("volunteer.html")


from flask import session, redirect, url_for

@app.route("/admin", methods=["GET","POST"])
def admin():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@pehchaan.org" and password == "pehchaan123":
            session["admin"] = True
            return redirect("/dashboard")

    return render_template("admin_login.html")

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/admin")

    return render_template("dashboard.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/")

def admin_required():
    if not session.get("admin"):
        return redirect("/admin")
    
@app.route("/admin/reports")
def admin_reports():

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    reports = conn.execute("SELECT * FROM reports").fetchall()
    conn.close()

    return render_template("rescue_reports.html", reports=reports)

@app.route("/admin/dogs")
def admin_dogs():

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    dogs = conn.execute("SELECT * FROM dogs").fetchall()
    conn.close()

    return render_template("dogs.html", dogs=dogs)

@app.route("/admin/adoptions")
def admin_adoptions():

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    adoptions = conn.execute("SELECT * FROM adoptions").fetchall()
    conn.close()

    return render_template("adoptions.html", adoptions=adoptions)

@app.route("/admin/volunteers")
def admin_volunteers():

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    volunteers = conn.execute("SELECT * FROM volunteers").fetchall()
    conn.close()

    return render_template("volunteers.html", volunteers=volunteers)

@app.route("/admin/approve/<int:id>")
def approve_volunteer(id):

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    conn.execute("UPDATE volunteers SET approved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin/volunteers")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
