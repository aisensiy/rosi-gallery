from flask import Flask

app = Flask('rosi-view')


@app.route("/")
def index():
    return file("index.html").read()

if __name__ == "__main__":
    app.run(debug=True)
