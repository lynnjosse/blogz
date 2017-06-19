from flask import Flask, request, redirect, render_template, session, flash
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'somerandomstring'




class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)    
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        #if pub_date is None:
        #    pub_date = date.today()
        #self.pub_date = pub_date

@app.route('/blog', methods=['GET', 'POST'])
def main_page():

    if request.args.get('id'):
        id = int(request.args.get('id'))
        blogs = [Blog.query.get(id)]



    else:
        blogs = Blog.query.all()

    return render_template('blog.html', title = "This Blog", blogs = blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def post_it(): 
    
    title = "New Post"

    return render_template('newpost.html' , title = title)
     
@app.route("/add", methods=['POST'])
def add_post():
    # look inside the request to figure out what the user typed
    new_post_title = request.form['title']
    new_post_body = request.form['blog']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_post_title) or (new_post_title.strip() == ""):
        print('HEREHEREHERE')
        flash("Your post must have a title.")
        return redirect ('/newpost')
        
    if (not new_post_body) or (new_post_body.strip() ==""):
        flash("Your post must have a body.")
        return redirect ('/newpost')

    new_post = Blog(new_post_title, new_post_body)
    db.session.add(new_post)
    db.session.commit()
    
    #find the id of the newly committed object

    current_post = Blog.query.filter_by(title = new_post_title).first()

    id = current_post.id
    
    return redirect ('/blog?id=' + str(id))



app.run()
