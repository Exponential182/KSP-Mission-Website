from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
database = "ksp.db"


@app.route("/")
def home():
    """ A Function to render the static home page to the site. """
    return render_template("home.html", title="KSP Mission Library")


@app.route("/missions")
def missions():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name, launch_vehicle, mission_goal, payload_image_reference FROM Mission ORDER BY name ASC")
    results = cursor.fetchall()
    print(results)
    return render_template("missions.html", title="KSP Mission Library", data=results)


# @app.route("/mission/<id:int>")
# def mission():
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
    

    
#     return render_template("mission.html", data = results)


@app.route("/engines")
def engines():
    return render_template("engines.html", title="KSP Mission Library")


@app.route("/stages")
def stages():
    return render_template("stages.html", title="KSP Mission Library")


@app.route("/license")
def license():
    """ A Function to render the mod license page. """
    return render_template("license.html", title="KSP Mission Library")


@app.route("/glossary")
def glossary():
    """ A Function to render the glossary of all used techinal terms. """
    return render_template("glossary.html", title="KSP Mission Library")


@app.route("/sitemap")
def sitemap():
    """ A function to render the sitemap, links to every
    non-paramertried query. 
    """
    return render_template("sitemap.html", title="KSP Mission Library")


@app.errorhandler(404)
def page_not_found_error(error):
    """ A Function to render the error page whena 404 error happens."""
    url = request.url
    return render_template("404.html", url = url), 404


if __name__ == '__main__':
    app.run(debug=True)