import sqlite3
from os import path

from flask import Flask, render_template, request

app = Flask(__name__)
# Generate the absolute path to the database to prevent the path leading 
# to the wrong database or creating an empty one and finding nothing.
runtime_directory = path.abspath(path.dirname(__file__))
db_path = path.join(runtime_directory, "ksp.db")


def lookup_query(query: str):
    """ A function to simplify the execution of pre-sanitised and 
    generated queries. 
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def mission_data_formatter(data_row: list):
    """ A Function to adjust the formatting of the data from the mission query 
    to a useful format.
    """
    # References are based on the databse structure so need to be updated if 
    # more columns are added to the database
    columns = [
        False, False, "Mission Goal", "Crew Count",
        "Estimated Mission Duration", "Power Source", "Axial Control System",
        False, False, "Launch Vehicle", "Destination", "Semi Major Axis (km)", 
        "Periapsis (km)", "Apoapsis (km)", "Orbital Period", "Eccentricity", 
        "Inclination (deg)", "Longitude of the Ascending Node (deg)",
        "Argument of Periapsis (deg)", "Latitude of Landing",
        "Longitude of Landing"
    ]
    meters_to_km = 0.001
    multiplicative_transforms = {
        11: meters_to_km, 12: meters_to_km, 13: meters_to_km, 
        14: seconds_to_time
    }
    for key, value in multiplicative_transforms.items():
        if callable(value) and data_row[key]: #Checks for a function reference.
            data_row[key] = value(data_row[key])
        elif isinstance(value, float) and isinstance(data_row[key], (int, float)):
            data_row[key] = round(data_row[key] * value, 3)
    formatted_datarow = list(zip(columns, data_row))
    return formatted_datarow


def seconds_to_time(seconds: float):
    """ A function to convert the any values of time in seconds into a
    ydhms (years, days, hours, minutes, seconds) format.
    """
    time_in_seconds = {31536000: "y", 86400: "d", 3600: "h", 60: "m"}
    output_time_string = ""
    for multiplier, time_string in time_in_seconds.items():
        if seconds // multiplier == 0:
            continue
        else:
            num_of_time_intervals = seconds // multiplier
            seconds -= num_of_time_intervals * multiplier
            output_time_string += f"{int(num_of_time_intervals)}{time_string} "
    if seconds > 0:
        output_time_string += f"{seconds:.2f}s"
    return output_time_string


@app.route("/")
def home():
    """ A Function to render the static home page to the site. """
    return render_template("home.html", title="KSP Mission Library")


@app.route("/missions")
def missions():
    """ A Function to render the dynamic page containing all of the missions 
    stored in the database.
    """
    query = """SELECT name, launch_vehicle, mission_goal, 
            payload_image_reference, id FROM Mission ORDER BY name ASC"""
    results = lookup_query(query)
    return render_template("missions.html", title="KSP Mission Library",
                           data=results, binary_true=True)


@app.route("/mission/<int:mission_id>")
def mission(mission_id: int):
    """ A Function to gather and format the data on a mission then render the 
    HTML template to display the mission data to the end user.
    """
    mission_query = f"SELECT * FROM Mission WHERE id = {mission_id}"
    results = lookup_query(mission_query)
    if len(results) > 0:
        results = list(results[0])
    else:
        return render_template("404.html", 
                               message="The id does not exist in the database.",
                               url = request.url)
    mission_info = mission_data_formatter(results)

    stages_query = ("SELECT id, name, length, top_diameter, bottom_diameter, "
                    "material, image_reference FROM Stage WHERE id in "
                    "(SELECT stage_id FROM MissionStage "
                    f"WHERE mission_id = {mission_id})")
    stages_info = lookup_query(stages_query)
    stages_info = [(a[0], a[1], a[2], round((a[3] + a[4])/2, 2), a[5], a[6]) for a in stages_info]


    return render_template("mission.html", title = "KSP Mission Library",
                           mission_data = mission_info, 
                           stages_data = stages_info)


@app.route("/engines")
def engines():
    """ A Function to render the dynamic page containing all of the enignes 
    stored in the database.
    """
    query = ("SELECT name, fuel_type, fuel_ratio, thrust_ASL, isp_Vac,"
            "ignition_count, image_reference, id FROM EngineORDER BY name ASC")
    results = lookup_query(query)
    return render_template("engines.html", title="KSP Mission Library",
                            data=results)


@app.route("/stages")
def stages():
    """ A Function to render the dynamic page containing all of the stages 
    stored in the database.
    """
    query = """SELECT id, name, length, top_diameter, bottom_diameter, 
            image_reference FROM Stage ORDER BY name ASC"""
    results = lookup_query(query)
    # Format the data to avoid computational logic in Jinja/HTML template.
    results = [(a[0], a[1], a[2], round((a[3] + a[4])/2, 2), a[5]) for a in results]
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
    """ A function to render the sitemap, which contains lnks to every page not
    defined by a procedurally generated query.
    """
    return render_template("sitemap.html", title="KSP Mission Library")


@app.errorhandler(404)
def page_not_found_error(error):
    """ A function to render the 404 page when an invalid link is caused."""
    url = request.url
    return render_template("404.html", message  = "The url does not exist.", url = url), 404


@app.errorhandler(500)
def internal_servef_error(error):
    """A function to render a page when there is a server side error."""
    return render_template("500.html")


if __name__ == '__main__':
    app.run(debug=True)