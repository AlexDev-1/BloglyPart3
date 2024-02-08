"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, check_table_exists, Post, Tag, PostTag
import os


username = os.environ["PGUSER"]
password = os.environ["PGPASSWORD"]
secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

app.app_context().push()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).all()
    tags = Tag().query.all()
    return render_template("posts/homepage.html", posts=posts , tags = tags)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# User route

@app.route('/users')
def list_users():
    """List of all users"""
    users = User().query.all()

    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def create_user():
    return render_template('users/addnew.html')
    
@app.route('/users/new', methods=["POST"])
def user_add():

    new_user  = User(first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.full_name} added.")

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/detail.html", user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_edit_post(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

##############################################################################
# Posts route

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tags = Tag().query.all()
    return render_template('posts/new.html', user=user, tags = tags )


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user = user, 
                    tags = tags)


    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag().query.all()

    return render_template("posts/detail.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag().query.all()
    return render_template('posts/edit.html', post=post, tags = tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tags_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags =  Tag.query.filter(Tag.id.in_(tags_ids)).all()

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

##############################################################################
# Tags route

@app.route('/tags')
def get_tags():

    tags = Tag().query.all()

    return render_template('/tags/list.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def get_tags_post(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('/tags/detail.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods = ["GET"])
def edit_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()


    return render_template('/tags/edit.html', tag = tag , posts = posts)

@app.route('/tags/<int:tag_id>/edit', methods = ["POST"])
def edit_tags_posted(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts =  Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"tag '{tag.name}' edited.")

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods = ["POST"])
def delete_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/new', methods= ['GET'])
def new_tag():
    
    posts = Post().query.all()

    return render_template('/tags/new.html', posts = posts)

@app.route('/tags/new', methods= ['POST'])
def new_tag_posted():

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name = request.form['name'], posts = posts)


    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag '{new_tag.name} create.")

    return redirect('/tags')

