from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
def load_data():
    # Replace 'data/matches.csv' with the path to your actual dataset
    try:
        data = pd.read_csv('data/matches.csv')
        return data
    except FileNotFoundError:
        return None

# Prediction logic
def predict_winner(team1, team2, data):
    if not team1 or not team2:
        return "Please enter both team names."

    if data is None or data.empty:
        return "Error: Dataset not found or empty."

    # Step 1: Calculate overall win rates
    team_stats = {}
    for _, row in data.iterrows():
        t1 = row['team1']
        t2 = row['team2']
        winner = row['winner']

        # Initialize stats for teams
        if t1 not in team_stats:
            team_stats[t1] = {'played': 0, 'won': 0}
        if t2 not in team_stats:
            team_stats[t2] = {'played': 0, 'won': 0}

        # Update played counts
        team_stats[t1]['played'] += 1
        team_stats[t2]['played'] += 1

        # Update win counts
        if winner == t1:
            team_stats[t1]['won'] += 1
        if winner == t2:
            team_stats[t2]['won'] += 1

    # Calculate win rates
    team1_win_rate = team_stats.get(team1, {'won': 0, 'played': 1})['won'] / team_stats.get(team1, {'played': 1})['played']
    team2_win_rate = team_stats.get(team2, {'won': 0, 'played': 1})['won'] / team_stats.get(team2, {'played': 1})['played']

    # Step 2: Calculate head-to-head win rates
    head_to_head = data[((data['team1'] == team1) & (data['team2'] == team2)) | 
                        ((data['team1'] == team2) & (data['team2'] == team1))]
    
    total_head_to_head = len(head_to_head)
    team1_head_to_head_wins = len(head_to_head[head_to_head['winner'] == team1])

    team1_head_to_head_rate = team1_head_to_head_wins / total_head_to_head if total_head_to_head > 0 else 0
    team2_head_to_head_rate = (total_head_to_head - team1_head_to_head_wins) / total_head_to_head if total_head_to_head > 0 else 0

    # Step 3: Combine scores (60% overall win rate, 40% head-to-head)
    team1_score = (0.6 * team1_win_rate) + (0.4 * team1_head_to_head_rate)
    team2_score = (0.6 * team2_win_rate) + (0.4 * team2_head_to_head_rate)

    # Step 4: Predict winner
    if team1 not in team_stats or team2 not in team_stats:
        return "One or both teams have no match history in the dataset."

    if team1_score > team2_score:
        return f"{team1} is predicted to win with a score of {(team1_score * 100):.2f}% vs {(team2_score * 100):.2f}%."
    elif team2_score > team1_score:
        return f"{team2} is predicted to win with a score of {(team2_score * 100):.2f}% vs {(team1_score * 100):.2f}%."
    else:
        return "The match is too close to call!"

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    data = load_data()

    if request.method == 'POST':
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        prediction = predict_winner(team1, team2, data)

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)