import sqlite3
from os import path

from flask import Flask, render_template, request

rounding_precision = 3
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


def numerical_type(input_variable):
    """ Checks if the variable is a numerical type (float or int) """
    if isinstance(input_variable, (float, int)):
        return True
    else:
        return False


def mission_data_formatter(data_row: list):
    """ Adjusts the formatting of the data from the mission query
    and pairs it to it's column name.
    """
    # References are based on the database structure so need to be updated if
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
        # Checks if a function reference or conversion factory is stored to
        # ensure that the correct operation is run
        if callable(value) and data_row[key]:
            data_row[key] = value(data_row[key])
        elif numerical_type(value) and numerical_type(data_row[key]):
            data_row[key] = round(data_row[key] * value, rounding_precision)
    formatted_data_row = list(zip(columns, data_row))
    return formatted_data_row


def engine_data_formatter(data_row: list):
    """ Adjusts the format of the data from the engine query to make the logic
    in the HTML template simpler.
    """
    # References are based on the database structure so need to be updated if
    # more columns are added to the database
    columns = [
        False, False, "Fuel Type", "Fuel Ratio", "Ignitions", "Pressure Fed",
        "Thrust (Sea Level) (kN)", "ISP (Sea Level) (s)",
        "Thrust (Vacuum) (kN)", "ISP (Vacuum) (s)", False
    ]
    # Converts if an engine is pressure fed from an integer to a word to make
    # it more descriptive.
    if data_row[5] == 0:
        data_row[5] = "No"
    elif data_row[5] == 1:
        data_row[5] = "Yes"
    formatted_data = list(zip(columns, data_row))
    return formatted_data


def stage_data_formatter(data_row: list):
    """ Adjusts the formatting of the data from the mission query
    and pairs it to it's column name.
    """
    # References are based on the database structure so need to be updated if
    # more columns are added to the database
    columns = [
        False, False, False, "Top Diameter", "Bottom Diameter",
        "Average Diameter", "Length", "Engine Count", "Tank Material/Type",
        False
    ]

    # Calculates the average stage diameter if possible otherwise returns N/A
    if numerical_type(data_row[3]) and numerical_type(data_row[4]):
        formatted_data = data_row[:5]
        formatted_data.append(round((data_row[3] + data_row[4])/2, 4))
        formatted_data.extend(data_row[5:])

    formatted_data = list(zip(columns, formatted_data))
    print(formatted_data)
    return formatted_data


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
    query: str = ("SELECT name, launch_vehicle, mission_goal,\
                  payload_image_reference, id FROM Mission ORDER BY name ASC")
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
        # Check if the result exists and turn it into a list for data

        results = list(results[0])
    else:
        return render_template("404.html",
                               message="The mission does not exist.",
                               url=request.url)
    mission_info = mission_data_formatter(results)

    stages_query: str = ("SELECT id, name, length, top_diameter,"
                         "bottom_diameter, material, image_reference FROM"
                         " Stage WHERE id in (SELECT stage_id FROM"
                         f" MissionStage WHERE mission_id = {mission_id})")
    stages_info = lookup_query(stages_query)
    if len(stages_info) > 0:
        new_stages_info = []
        for data in stages_info:
            if (isinstance(data[3], (int, float)) and
                    isinstance(data[4], (int, float))):
                new_stages_info.append(
                    (data[0], data[1], data[2],
                     round((data[3]+data[4])/2, rounding_precision), data[5],
                     data[6])
                )
            else:
                new_stages_info.append(
                    (data[0], data[1], data[2], "N/A", data[5], data[6])
                )
        stages_info = new_stages_info

    images_query: str = ("SELECT caption, url, id FROM Image WHERE id in"
                         "(SELECT image_id FROM MissionImage WHERE mission_id"
                         f" = {mission_id})")
    images_info = lookup_query(images_query)
    if len(images_info) > 0:
        images_info = [
            (image[0], image[1], index+1) for index, image in
            enumerate(images_info)
        ]

    return render_template("mission.html", title="KSP Mission Library",
                           mission_data=mission_info,
                           stages_data=stages_info,
                           image_gallery_data=images_info)


@app.route("/engines")
def engines():
    """ A Function to render the dynamic page containing all of the engines
    stored in the database.
    """
    query: str = ("SELECT name, fuel_type, fuel_ratio, thrust_ASL, isp_Vac,"
                  "ignition_count, image_reference, id FROM Engine ORDER BY"
                  " name")
    results = lookup_query(query)
    return render_template("engines.html", title="KSP Mission Library",
                           data=results)


@app.route("/engine/<int:engine_id>")
def engine(engine_id):
    """ Collect the data for and render the engine specific page."""
    engine_query = f"SELECT * FROM Engine WHERE id = {engine_id}"
    engine_results = lookup_query(engine_query)
    if len(engine_results) > 0:
        engine_results = list(engine_results[0])
    else:
        return render_template("404.html", url=request.url,
                               message="The engine does not exist.")

    engine_data = engine_data_formatter(engine_results)
    return render_template("engine.html", title="KSP Mission Library",
                           engine_data=engine_data)


@app.route("/stages")
def stages():
    """ A Function to render the dynamic page containing all of the stages
    stored in the database.
    """
    query: str = ("SELECT id, name, length, top_diameter, bottom_diameter,"
                  "image_reference FROM Stage ORDER BY name ASC")
    results = lookup_query(query)
    # Format the data to avoid computational logic in Jinja/HTML template.
    formatted_results = [
        (r[0], r[1], r[2], round((r[3] + r[4])/2, 2), r[5]) for r in results
    ]
    return render_template("stages.html", title="KSP Mission Library",
                           data=formatted_results)


@app.route("/stage/<int:stage_id>")
def stage(stage_id: int):
    """ Collect the data for and render the stage specific page."""
    stage_query = f"SELECT * FROM Stage WHERE id = {stage_id}"
    stage_results = lookup_query(stage_query)
    if len(stage_results) > 0:
        stage_results = list(stage_results[0])
    else:
        return render_template("404.html",
                               message="The stage does not exist.",
                               url=request.url)

    stage_results = stage_data_formatter(stage_results)

    engine_query: str = ("SELECT name, fuel_type, fuel_ratio, thrust_ASL,"
                         "isp_Vac, ignition_count, image_reference, id FROM "
                         "Engine WHERE id in (SELECT engine_id FROM "
                         f"StageEngine WHERE stage_id = {stage_id})")
    engine_results = lookup_query(engine_query)

    return render_template("stage.html", title="KSP Mission Library",
                           stage_data=stage_results,
                           engine_data=engine_results)


@app.route("/license")
def license():
    """ A Function to render the mod license page."""
    return render_template("license.html", title="KSP Mission Library")


@app.route("/glossary")
def glossary():
    """ A Function to render the glossary of all used technical terms. """
    return render_template("glossary.html", title="KSP Mission Library")


@app.errorhandler(404)
def page_not_found_error(error):
    """ A function to render the 404 page when a page cannot be rendered or
    found."""
    url = request.url
    message = "The url does not exist/is invalid."
    return render_template("404.html", message=message,
                           url=url), 404


@app.errorhandler(500)
def internal_server_error(error):
    """A function to render a page when there is a server side error."""
    return render_template("500.html")


if __name__ == '__main__':
    app.run(debug=True)
