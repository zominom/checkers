from flask import Flask, render_template, request, session, jsonify, redirect
from flask_session import Session

from datetime import timedelta

import sys
sys.path.append(r'C:\Users\test0\OneDrive\שולחן העבודה\checkers\web\checkers_game')
sys.path.append(r'C:\Users\test0\OneDrive\שולחן העבודה\checkers\web\checkers_bot')

from checkers_logic import Game
from bot_logic import Bot

app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"  ] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=40)
app.config['SESSION_FILE_THRESHOLD'] = 100
Session(app)

@app.route("/")
def index():
    if 'game_state' in session.keys():
        game = Game.deserialize(session['game_state'])
    else:
        game = Game()
        session['game_state'] = game.serialize()

    return render_template('checkers.html', game_state=game.serialize())
 
@app.route('/make_move', methods=['POST'])
def make_move():
    if 'game_state' not in session.keys():
        return redirect('/')

    move = request.json['move']

    game = Game.deserialize(session['game_state'])
    
    if not game.make_move(move):
        return jsonify(game_state=game.serialize(), error="Not a valid move")

    winner = game.get_winner()
    if winner is not None:
        session.clear()
        return jsonify(game_state=game.serialize(), error=f"{"WHITE" if winner is Game.WHITE else "BLACK"} is the winner")

    session['game_state'] = game.serialize()
    return jsonify(game_state=game.serialize(), error=None)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    depth = request.json['depth']
    if 'game_state' in session:
        game = Game.deserialize(session['game_state'])
        return jsonify(move=str(Bot(game).get_minimax_move(depth, True)))
    
@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)