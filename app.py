from flask import Flask,render_template,url_for
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.route('/movies')
def movies():
    movies = []
    for i in range(1, 10):
        movies.append({
            'movieName':'Last'
        })
    return render_template('movies.html',movies = movies)

if __name__ == '__main__':
    app.run(port=5004,debug=True)