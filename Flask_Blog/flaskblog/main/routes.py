from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    selected_tags = request.args.getlist('tags')
    sort_option = request.args.get('sort', 'latest')
    category = request.args.get('category', 'main')
    query = Post.query.filter_by(category=category)
    for tag in selected_tags:
        query = query.filter(Post.tags.contains(tag))
    if sort_option == 'oldest':
        query = query.order_by(Post.date_posted.asc()) 
    else:
        query = query.order_by(Post.date_posted.desc())
    posts = query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts, current_category='main')

@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    selected_tags = request.args.getlist('tags')
    sort_option = request.args.get('sort', 'latest')
    category = request.args.get('category', 'blog')
    query = Post.query.filter_by(category=category)
    for tag in selected_tags:
        query = query.filter(Post.tags.contains(tag))
    if sort_option == 'oldest':
        query = query.order_by(Post.date_posted.asc()) 
    else:
        query = query.order_by(Post.date_posted.desc())
    posts = query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts, current_category='blog')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
