"""
Game Management System
----------------------

A Flask-based web application for managing a large board game collection and tracking borrowed/available games.

⚠️ Disclaimer:
- This is for **personal use and learning purposes**.
- The admin login currently uses a hardcoded username/password.
- This is not secure and will be replaced with proper authentication in the future.

Features (current + planned):
- Maintain a list of games (available vs checked out).
- Allow Friends to scan QR code to access to the site.
- User checkout form for borrowing games.
- Admin page with basic login, add/view/filter games.

Tech Stack:
- Flask (Python), SQLite, HTML/CSS, JavaScript, Render(Deployment)

Status:
Work in progress. Future updates will improve security and add professional-grade features.
"""


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boardgames.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Game model
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')

# Borrower model (1:1 relationship with Game enforced logically)
class Borrower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    borrowed_game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    borrow_date = db.Column(db.DateTime, nullable=False)
    game = db.relationship('Game', backref=db.backref('borrowers', lazy=True))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/checkout')
def checkout():
    games = Game.query.filter_by(status='available').all()
    return render_template('checkout.html', games=games)

@app.route('/borrow', methods=['POST'])
def borrow():
    name = request.form['name']
    borrow_date = request.form['date']
    game_id = request.form['game_id']

    borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')
    game = Game.query.get(game_id)

    if game.status != 'available':
        return "This game is already checked out.", 400

    new_borrower = Borrower(name=name, borrowed_game_id=game.id, borrow_date=borrow_date)
    game.status = 'Checked out'

    db.session.add(new_borrower)
    db.session.commit()

    return render_template('checkedOut.html')

@app.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    username = "kcbandrew"
    password = "00000"

    if request.method == 'POST':
        login1 = request.form.get('login-username')
        login2 = request.form.get('login-password')

        if login1 == username and login2 == password:
            return redirect(url_for('admin_backend'))
        else:
            return render_template('adminLogin.html', error='Invalid username or password')

    return render_template('adminLogin.html')

@app.route('/adminBackend', methods=['GET', 'POST'])
def admin_backend():
    if request.method == 'POST':
        game_id = request.form.get('game_id')
        new_status = request.form.get('status')
        game = Game.query.get(game_id)

        if game:
            game.status = new_status

            if new_status == 'available':
                # Remove any borrower record for this game
                Borrower.query.filter_by(borrowed_game_id=game.id).delete()

            db.session.commit()

    games = Game.query.all()

    # Get the latest borrower (if any) for each game
    borrowers = {
        g.id: Borrower.query.filter_by(borrowed_game_id=g.id).order_by(Borrower.borrow_date.desc()).first()
        for g in games
    }

    return render_template('adminBackend.html', games=games, borrowers=borrowers)


@app.route('/addGame', methods=['POST'])
def add_game():
    game_title = request.form.get('game_title')
    new_game = Game(title=game_title, status='available')
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('admin_backend'))

@app.route('/removeGame', methods=['POST'])
def remove_game():
    game_id = request.form.get('game_id')
    game_to_remove = Game.query.get(game_id)
    if game_to_remove:
        Borrower.query.filter_by(borrowed_game_id=game_id).delete()
        db.session.delete(game_to_remove)
        db.session.commit()
    return redirect(url_for('admin_backend'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
