from flask import Flask, jsonify
from config import Config
from extensions import db
from routes.event_routes import event_bp
from routes.auth_routes import auth_bp

from routes.admin_routes import admin_bp

from flask import render_template

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(event_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

app.register_blueprint(admin_bp, url_prefix="/api/admin")


@app.route("/")
def home():
    return jsonify({"message": "Cyber Security API running"})

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/activity")
def activity_page():
    return render_template("activity.html")

@app.route("/admin/user-profile/<int:user_id>")
def user_profile(user_id):
    return render_template("user_profile.html", user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
