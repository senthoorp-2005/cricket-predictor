# Cricket Match Predictor

A simple Flask app to predict the winner of a cricket match based on historical data.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cricket-predictor
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Ensure your dataset is in `data/matches.csv`. The app expects at least `team1`, `team2`, and `winner` columns.

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`.

## Usage

- Enter the names of two teams in the input fields.
- Click "Predict Winner" to see the prediction.

## Deployment

To deploy on a server (e.g., Heroku, Render), follow their respective deployment guides for Flask apps.