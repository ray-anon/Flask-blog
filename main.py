from website import create_app
from flask import render_template
app = create_app()

@app.errorhandler(404)
def error404(e):
    return render_template("404.html")

@app.errorhandler(500)
def error500(e):
    return render_template("505.html")


if __name__ == '__main__':
    app.run(debug=True)