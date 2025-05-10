from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="KSP Mission Library")


@app.route("/missions")
def missions():
    return render_template("missions.html", title="KSP Mission Library")


@app.route("/engines")
def engines():
    return render_template("engines.html", title="KSP Mission Library")


@app.route("/stages")
def stages():
    return render_template("stages.html", title="KSP Mission Library")


@app.errorhandler(404)
def page_not_found_error(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)