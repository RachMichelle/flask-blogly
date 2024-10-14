from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'bloglyapp'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """show home page"""

    posts=Post.query.order_by(Post.created_at).limit(5)
    return render_template('home.html', posts=posts)

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

# ** Foreign key error for posts table. Cascade delete?

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
    tags = post.tgs
    return render_template('post.html', post=post, tags=tags)

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

# ** Error on delete for posts_tags table foreign key constraint

@app.route('/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    """delete post with associated post id, redirect back to user info page"""

    post=Post.query.get(post_id)
    user_id=post.usr.id

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f'/user/{user_id}')

@app.route('/tags')
def tags_list():
    """show list of all tags"""

    tags=Tag.query.order_by('name')

    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def new_tag():
    """show form to add tag"""

    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def handle_new_tag():
    
    name = request.form['name']

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>')
def show_tag_info(tag_id):
    """shows list of posts with assocated tag"""

    tag= Tag.query.get(tag_id)
    posts=tag.psts

    return render_template('tag-info.html', posts=posts, tag=tag)

@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """show form to edit tag with associated id"""

    tag= Tag.query.get(tag_id)

    return render_template('tag-edit.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """submit changes from edit tag form"""

    tag= Tag.query.get(tag_id)

    name= request.form['name']

    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")


# ** getting foreign key error for posts_tags table ** 

# @app.route('/delete/<tag_id>', methods=['POST'])
# def handle_delete_tag(tag_id):
#     """delete tag with associated id"""

#     Tag.query.filter_by(id=tag_id).delete()

#     db.session.commit()

#     return redirect('/tags')