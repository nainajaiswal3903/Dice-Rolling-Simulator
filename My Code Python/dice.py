# dice_art.py

dice_art = {
    1: ["┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"],
    2: ["┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"],
    3: ["┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"],
    4: ["┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"],
    5: ["┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"],
    6: ["┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"]
}

# app.py

from flask import Flask, render_template, request
import random
from dice_art import dice_art

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dice = []
    total = 0
    num_of_dice = 0

    if request.method == 'POST':
        num_of_dice = int(request.form['num_of_dice'])
        for _ in range(num_of_dice):
            dice.append(random.randint(1, 6))
        total = sum(dice)
        
    dice_rendered = []
    if dice:
        for i in range(5):
            row = ""
            for d in dice:
                row += dice_art[d][i] + " "
            dice_rendered.append(row)
    return render_template('index.html', dice=dice_rendered, total=total, num_of_dice=num_of_dice)

if __name__ == '__main__':
    app.run(debug=True)
