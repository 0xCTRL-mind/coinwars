from flask import Flask, render_template, request, redirect, url_for, session
from coinwars import Game  # Import the Game class from your existing file

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game = Game()
    session['game'] = game.__dict__  # Store the game state in the session
    return redirect(url_for('play_game'))

@app.route('/play_game', methods=['GET', 'POST'])
def play_game():
    if 'game' not in session:
        return redirect(url_for('home'))
    
    game = Game()
    game.__dict__ = session['game']  # Restore the game state from the session

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'buy':
            item = request.form.get('item')
            quantity = int(request.form.get('quantity'))
            result = game.buy(item, quantity)
        elif action == 'sell':
            item = request.form.get('item')
            quantity = int(request.form.get('quantity'))
            result = game.sell(item, quantity)
        elif action == 'next_turn':
            game.play_turn()
        
        session['game'] = game.__dict__  # Update the game state in the session

    return render_template('play_game.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)
