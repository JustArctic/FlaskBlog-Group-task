from flask import Flask, render_templete
app = Flask (__name__)

posts = [
    {
        'author': 'Allan Luong',
        'title': 'Blog Post 1'
        'content': 'first post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Danny Trieu Nguyen',
        'title': 'Blog Post 2'
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home") 
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return "<hi>About Page</hi>"


if __name__ == '__main__':
    app,run(debug=True)