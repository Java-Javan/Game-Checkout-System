from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Set up the SQLite database URI

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boardgames.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # creates boardgames.bd in the project folder

# Initialize the DataBase
db = SQLAlchemy(app)


# create Data Tables
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')


class Borrower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # User's name
    borrowed_game_id = db.Column(db.Integer, db.ForeignKey('game.id'))  # The game ID (foreign key)
    borrow_date = db.Column(db.DateTime, nullable=False)  # The date they borrowed the game
    game = db.relationship('Game', backref=db.backref('borrowers', lazy=True))  # Relationship with Game model




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/checkout')
def checkout():
    games = Game.query.filter_by(status='available').all()  # Display all games that have the status of available
    return render_template('checkout.html', games=games)


@app.route('/borrow', methods = ['POST', 'GET'])
def borrow():

    # Get the data from the user submitted form
    name = request.form['name']
    borrow_date = request.form['date']
    game_id = request.form['game_id']

    # Convert the Date from a String to a Datetime
    borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')

    #find the game in the database

    game = Game.query.get(game_id)

    #Create a new Borrower entry

    new_borrower = Borrower(name=name, borrowed_game_id = game.id, borrow_date = borrow_date)

    #update the games status

    game.status = 'Checked out'

    # add and commit to the database
    db.session.add(new_borrower)
    db.session.commit()

    return render_template('checkedOut.html')  # come back to this once the success page is completed

@app.route('/adminLogin' , methods=['GET', 'POST'])
def admin_login():
    username = "kcbandrew"
    password = "00000"

    if request.method == 'POST':
        #Get the data from the form
        login1 = request.form.get('login-username')
        login2 = request.form.get('login-password')

        #Check Credentials
        if login1 == username and login2 == password:
            return redirect(url_for('admin_backend'))
        else:
            return render_template('adminLogin.html', error='Invalid username or password')

    return render_template('adminLogin.html')


@app.route('/adminBackend', methods=['GET', 'POST'])
def admin_backend():
    if request.method == 'POST':
        # Get form data to update the game's status
        game_id = request.form.get('game_id')
        new_status = request.form.get('status')

        # Find the game and update the status
        game = Game.query.get(game_id)
        if game:
            game.status = new_status
            db.session.commit()

    # query all games
    games = Game.query.all()
    # query all borrowers
    borrowers = Borrower.query.all()

    # pass the data into the admin backend html template
    return render_template('adminBackend.html', games=games, borrowers=borrowers)

@app.route('/addGame', methods=['POST'])
def add_game():
     # Get the game title from the form
     game_title = request.form.get('game_title')

     # Create a new Game object
     new_game = Game(title=game_title, status='available')

     # Add the new game to the database
     db.session.add(new_game)
     db.session.commit()

     # redirect ack to the admin backend form
     return redirect(url_for('admin_backend'))


@app.route('/removeGame', methods=['GET', 'POST'])
def remove_game():

    #get the game title from the form
    game_id = request.form.get('game_id')

    #FInd the game in the database by its id
    game_to_remove = Game.query.get(game_id)
    if game_to_remove:
        # remove the game form the database
        db.session.delete(game_to_remove)
        db.session.commit()

    # Redirect to the admin backend form
    return redirect(url_for('admin_backend'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
