import os

from flask import Flask, render_template, request, redirect, url_for 
#from .import db
#from .import auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    #moved from App.py 
    @app.route('/')
    def index():
        return redirect(url_for('home'))

    @app.route('/home')
    def home():
        # our wireframe flow is: home (not logged in) -> login -> home (logged in)
        # see flask.palletsprojects.com -> tutorial -> "require authentication" (i think)
        # for now, just view home page
        return render_template('home.html')

    # nove to auth.py @app.route('/login', methods=['GET', 'POST'])
    def login():
        # note: with the change to home being the first page visited,
        # the login form needs to direct to home, or maybe home_loggedin, idk
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if check_user(username, password):
                return redirect(url_for('secret'))
            else:
                return 'Invalid username/password combination'
        return render_template('login.html')

    @app.route('/secret')
    def secret():
        return 'You have logged in successfully!'

    def add_user(username, password):
        with open('users.pkl', 'ab') as f:
            pickle.dump({username: password}, f)

    def check_user(username, password):
        with open('users.pkl', 'rb') as f:
            while True:
                try:
                    user = pickle.load(f)
                    if username in user and user[username] == password:
                        return True
                except EOFError:
                    break
        return False

    #move to auth.py @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if check_user(username, password):
                return 'User already exists'
            add_user(username, password)
            return redirect(url_for('login'))
        return render_template('register.html')
    from . import db    
    db.init_app(app)
    
    
    from . import auth   
    app.register_blueprint(auth.bp)

    return app