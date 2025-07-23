from flask import Flask, render_template, request
import sqlite3
from os import path

app = Flask(__name__)
runtime_directory = path.abspath(path.dirname(__file__))
db_path = path.join(runtime_directory, "ksp.db")


def lookup_query(query: str):
    """ A function to simplify the execution of pre-sanitised queries. """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def mission_data_formatter(data_row: list):
    """ A Function to adjust the formatting of the data from the mission query 
    to a useful format.
    """
    columns = [
        False, False, "Mission Goal", "Crew Count",
        "Estimated Mission Duration", "Power Source", "Axial Control System",
        False, False, "Launch Vehicle", "Destination", "Semi Major Axis (km)", 
        "Periapsis (km)", "Apoapsis (km)", "Orbital Period", "Eccentricity", 
        "Inclination (deg)", "Longitude of the Ascending Node (deg)",
        "Argument of Periapsis (deg)", "Latitude of Landing",
        "Longitude of Landing"
    ]
    m_to_km = 0.001
    multiplicative_transforms = {
        11: m_to_km, 12: m_to_km, 13: m_to_km, 14: seconds_to_time,
    }
    for key, value in multiplicative_transforms.items():
        if callable(value) is True and data_row[key]:
            data_row[key] = value(data_row[key])
        elif type(value) == float and type(data_row[key]) == (float or int):
            data_row[key] = round(data_row[key] * value, 3)
    formatted_datarow = list(zip(columns, data_row))
    return formatted_datarow


def seconds_to_time(seconds: float):
    time_in_seconds = {31536000: "y", 86400: "d", 3600: "h", 60: "m"}
    output_time_string = ""
    for mult, time_string in time_in_seconds.items():
        print(seconds)
        if seconds // mult == 0:
            continue
        else:
            num_of_time_intervals = seconds // mult
            seconds -= num_of_time_intervals * mult
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
    orbital_parameter_and_landing_columns = [
        "Semi Major Axis (km)", 
        "Periapsis (km)", "Apoapsis (km)", "Orbital Period", "Eccentricity", 
        "Inclination", "Longitude of the Ascending Node",
        "Argument of Periapsis", "Latitude of Landing", "Longitude of Landing"
    ]
    query = f"SELECT * FROM Mission WHERE id = {mission_id}"
    results = lookup_query(query)
    if len(results) > 0:
        results = list(results[0])
    else:
        return render_template("404.html", message= "The id does not exist in the database.", url = request.url)
    
    results = mission_data_formatter(results)

    return render_template("mission.html", title = "KSP Mission Library", mission_data = results)


@app.route("/engines")
def engines():
    """ A Function to render the dynamic page containing all of the enignes 
    stored in the database.
    """
    query = """SELECT name, fuel_type, fuel_ratio, thrust_ASL, isp_Vac,
                   ignition_count, image_reference, id FROM Engine
                   ORDER BY name ASC"""
    results = lookup_query(query)
    return render_template("engines.html", title="KSP Mission Library",
                            data=results)


@app.route("/stages")
def stages():
    """ A Function to render the dynamic page containing all of the stages 
    stored in the database.
    """
    query = """SELECT name, length, top_diameter, bottom_diameter, 
            image_reference, id FROM Stage ORDER BY name ASC"""
    results = lookup_query(query)
    results = [(a[0], a[1], round((a[2] + a[3])/2, 2), a[4], a[5]) for a in results]
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
    return render_template("404.html", message  = "The url does not exist.", url = url), 404


if __name__ == '__main__':
    app.run(debug=True)