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
    """ A Function to render the dynamic page containing all of the missions 
    stored in the database.
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT name, launch_vehicle, mission_goal, 
                   payload_image_reference, id FROM Mission 
                   ORDER BY name ASC""")
    results = cursor.fetchall()
    return render_template("missions.html", title="KSP Mission Library",
                            data=results)


# @app.route("/mission/<id:int>")
# def mission():
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#     return render_template("mission.html", data = results)


@app.route("/engines")
def engines():
    """ A Function to render the dynamic page containing all of the enignes 
    stored in the database.
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT name, fuel_type, fuel_ratio, thrust_ASL, isp_Vac,
                   ignition_count, image_reference, id FROM Engine
                   ORDER BY name ASC""")
    results = cursor.fetchall()
    print(results)
    return render_template("engines.html", title="KSP Mission Library",
                            data=results)


@app.route("/stages")
def stages():
    """ A Function to render the dynamic page containing all of the stages 
    stored in the database.
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT name, length, top_diameter, bottom_diameter, 
                   image_reference, id FROM Stage ORDER BY name ASC""")
    results = cursor.fetchall()
    print(results)
    results = [(a[0], a[1], round((a[2] + a[3])/2, 2), a[4], a[5]) for a in results]
    print(results)
    return render_template("stages.html", title="KSP Mission Library",
                           data=results)


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