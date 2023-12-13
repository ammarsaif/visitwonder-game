from flask import Flask, render_template, request
import geopy.distance
from queries import insert, select, update
from main import run_game

app = Flask(__name__)

destinations = {
    1: "Parthenon",
    2: "Easter Island",
    3: "Taj Mahal",
    4: "Colosseum",
    5: "Angkor",
    6: "Teotihuacan",
    7: "Petra",
    8: "Machu Picchu",
    9: "Great Wall of China",
    10: "Pyramids of Giza",
    11: "Stonehenge",
    12: "Hagia Sophia",
    13: "Chichen Itza",
    14: "Easter Islands",
    15: "Persepolis",
    16: "The Mezquita of Córdoba"
}

# Define your game difficulty and win thresholds
difficulty_easy = 10000
difficulty_medium = 12000
difficulty_hard = 16000
game_win_easy = 7
game_win_medium = 10
game_win_hard = 14


def set_difficulty(difficulty, player_email):
    update.update_difficulty(difficulty, player_email)


@app.route('/')
def home():
    return render_template('index.html')  # Create an HTML file for the home page


@app.route('/start_game', methods=['POST'])
def start_game():
    if request.method == 'POST':
        want_to_play = request.form.get('play')
        if want_to_play.lower() == 'yes':
            return render_template('index.html')  # Create an HTML file for difficulty selection
        else:
            return render_template('index.html')  # Create an HTML file for goodbye message


@app.route('/select_difficulty', methods=['POST'])
def select_difficulty():
    if request.method == 'POST':
        difficulty_level = request.form.get('difficulty')
        player_email = request.form.get('email')

        if difficulty_level.lower() == "easy":
            difficulty = difficulty_easy
            set_difficulty(difficulty, player_email)
            game_win_threshold = game_win_easy
        elif difficulty_level.lower() == "medium":
            difficulty = difficulty_medium
            set_difficulty(difficulty, player_email)
            game_win_threshold = game_win_medium
        elif difficulty_level.lower() == "hard":
            difficulty = difficulty_hard
            set_difficulty(difficulty, player_email)
            game_win_threshold = game_win_hard

        return render_template('index.html', destinations=destinations, difficulty=difficulty)


@app.route('/play_game', methods=['POST'])
def play_game():
    if request.method == 'POST':
        player_email = request.form.get('email')
        difficulty = request.form.get('difficulty')
        game_win_threshold = request.form.get('game_win_threshold')

        # Call the run_game function with the necessary parameters
        run_game(player_email, difficulty, game_win_threshold)

        return render_template('index.html')  # Create an HTML file for displaying game results


if __name__ == '__main__':
    app.run(debug=True)
