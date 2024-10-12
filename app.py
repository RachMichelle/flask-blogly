from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'bloglyapp'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """redirects to users page"""

    return redirect('/users')

@app.route('/users')
def user_list():
    """shows list of all users"""

    users = User.query.order_by('last_name')
    
    return render_template('users.html', users=users)

@app.route('/user/<user_id>')
def show_user_info(user_id):
    """show info for user associated with user id"""

    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template('user-info.html', user=user, posts=posts)


@app.route('/user/<user_id>/edit', methods=['POST'])
def handle_edit_user(user_id):
    """submit edit user form info & redirect to users list"""

    user = User.query.get(user_id)
    user_id= user.id

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user.first_name = first_name
    user.last_name = last_name
    if img_url == '':
        user.img_url = None
    else:
        user.img_url = img_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/user/<user_id>/edit')
def edit_user(user_id):
    """show edit user form"""

    user = User.query.get(user_id)
    return render_template('user-edit.html', user=user)

@app.route('/users/new')
def new_user():
    """show new user form"""

    return render_template('/new-user.html')

@app.route('/users/new', methods=['POST'])
def handle_new_user():
    """submit new user form & redirect to users list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    if img_url != '':
        user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    else:
        user= User(first_name=first_name, last_name=last_name)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/delete/<user_id>', methods = ['POST'])
def delete_user(user_id):
    """delete a user"""

    User.query.filter_by(id=user_id).delete()

    db.session.commit()
    
    return redirect('/users')

@app.route('/posts/<post_id>')
def show_post(post_id):
    """shows full post details for associated post id"""

    post = Post.query.get(post_id)

    return render_template('post.html', post=post)

@app.route('/user/<user_id>/posts/new')
def new_post(user_id):
    """show form to add a new post"""

    user = User.query.get(user_id)

    return render_template('new-post.html', user=user)

@app.route('/user/<user_id>/posts/new', methods=['POST'])
def handle_new_post(user_id):
    """add new post to db on submit"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/user/{user_id}')

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """show form to edit existing post """

    post = Post.query.get(post_id)

    return render_template('post-edit.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """submit edits to associated post"""

    post = Post.query.get(post_id)

    title = request.form['title']
    content = request.form['content']

    post.title=title
    post.content=content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/delete/<post_id>')
def delete_post(post_id):
    """delete post with associated post id, redirect back to user info page"""

    post=Post.query.get(post_id)
    user_id=post.usr.id

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f'/user/{user_id}')