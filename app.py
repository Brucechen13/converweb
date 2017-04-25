from flask import Flask,render_template,url_for
from flask.ext.bootstrap import Bootstrap
from movieSpide import getMovie
from musicSpide import getMusic

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
    return render_template('movies.html',movies = movies)


@app.route('/musics')
def musics():
    return render_template('music.html',musics = musics)

if __name__ == '__main__':
    movies = getMovie() 
    musics = getMusic() 
    app.run(port=5002,debug=True)