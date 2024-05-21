from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}

players_scores = []
player_names = []
current_player_index = 0
total_turns = 0
max_turns_per_player = 5

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roll_dice', methods=['GET'])
def roll_dice():
    global current_player_index, total_turns

    current_player = player_names[current_player_index]
    dice = [random.randint(1, 6) for _ in range(2)]
    total = sum(dice)
    dice_faces = [dice_art[die] for die in dice]
    
    players_scores[current_player_index].append(total)
    total_turns += 1

    if total_turns % len(player_names) == 0:
        current_player_index = 0
    else:
        current_player_index = (current_player_index + 1) % len(player_names)

    return jsonify({
        'dice_faces': dice_faces,
        'total': total,
        'player': current_player,
        'total_turns': total_turns
    })

@app.route('/set_players', methods=['POST'])
def set_players():
    global player_names, players_scores, current_player_index, total_turns

    player_names = request.json.get('names', [])
    players_scores = [[] for _ in range(len(player_names))]
    current_player_index = 0
    total_turns = 0
    return jsonify({'status': 'success'})

@app.route('/get_scores', methods=['GET'])
def get_scores():
    scores = {player_names[i]: sum(scores) for i, scores in enumerate(players_scores)}
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    winner = sorted_scores[0][0]
    return jsonify({'scores': scores, 'winner': winner})

@app.route('/restart', methods=['POST'])
def restart():
    global players_scores, player_names, current_player_index, total_turns

    players_scores = []
    player_names = []
    current_player_index = 0
    total_turns = 0
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
