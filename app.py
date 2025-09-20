from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # owners login session kosam

# Database init
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  food_item TEXT,
                  rating INTEGER,
                  comment TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Feedback form
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        food_item = request.form["food_item"]
        rating = request.form["rating"]
        comment = request.form["comment"]

        conn = sqlite3.connect("feedback.db")
        c = conn.cursor()
        c.execute("INSERT INTO feedback (name, food_item, rating, comment) VALUES (?, ?, ?, ?)",
                  (name, food_item, rating, comment))
        conn.commit()
        conn.close()
        return redirect("/feedbacks")  # optional: redirect to owners page
    return render_template("feedback.html")

# Owner login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["logged_in"] = True
            return redirect("/feedbacks")
        else:
            error = "Invalid Credentials. Try again."
    return render_template("login.html", error=error)

# Owner logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/")

# Display all feedbacks (only owner)
@app.route("/feedbacks")
def feedbacks():
    if not session.get("logged_in"):
        return redirect("/login")
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    data = c.fetchall()
    conn.close()
    return render_template("feedback_list.html", feedbacks=data)

# Delete feedback (only owner)
@app.route("/delete/<int:fb_id>")
def delete_feedback(fb_id):
    if not session.get("logged_in"):
        return redirect("/login")
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id=?", (fb_id,))
    conn.commit()
    conn.close()
    return redirect("/feedbacks")

if __name__ == "__main__":
    app.run(debug=True)

