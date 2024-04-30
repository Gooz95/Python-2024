# https://code.tutsplus.com/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972t

from flask import Flask, render_template, request
from siwel_files import siwel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/classes/')
def classes():
    return render_template('classes.html')

@app.route('/services/')
def services():
    return render_template('services.html')

@app.route('/about/')
def about():
    return render_template('about.html')


# lewis added:
@app.route('/test/')
def test():
    return siwel.return_html()


if __name__ == "__main__":
    app.run(debug=True)
