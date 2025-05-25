# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from blockchain_core import Blockchain

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

# --- USER DATA MANAGEMENT ---
USERS_FILE = 'users.json'


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:  # Handle empty or corrupted file
        return {}


def save_users(users_data):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=4)


# --- BLOCKCHAIN INSTANCE ---
blockchain = Blockchain()


# --- ROUTES ---
@app.route('/')
def home():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    users = load_users()
    user_data = users.get(session['user_email'])

    # Check if user_data exists, if not, something is wrong, log out.
    if not user_data:
        session.pop('user_email', None)
        flash('User data not found. Please log in again.', 'error')
        return redirect(url_for('login'))

    return render_template('index.html',
                           candidates=list(blockchain.candidates.keys()),
                           has_voted=user_data.get('has_voted', False),
                           pending_votes_count=len(blockchain.pending_votes),
                           results=blockchain.get_results(),
                           user_email=session['user_email'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        users[email] = {'password_hash': hashed_password, 'has_voted': False,
                        'is_admin': False}  # New users are not admin
        # Make first registered user an admin (optional for MVP)
        # if len(users) == 1:
        #     users[email]['is_admin'] = True

        save_users(users)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        user_data = users.get(email)

        if user_data and check_password_hash(user_data['password_hash'], password):
            session['user_email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    if 'user_email' not in session:
        flash('Please login to vote.', 'error')
        return redirect(url_for('login'))

    voter_email = session['user_email']
    candidate_choice = request.form.get('candidate_choice')
    users = load_users()
    user_data = users.get(voter_email)

    if not user_data:  # Should not happen if session is valid
        flash('User not found. Please re-login.', 'error')
        session.pop('user_email', None)
        return redirect(url_for('login'))

    if user_data.get('has_voted', False):
        flash('You have already voted.', 'warning')
        return redirect(url_for('home'))

    if not candidate_choice:
        flash('Please select a candidate.', 'warning')
        return redirect(url_for('home'))

    message = blockchain.add_vote_to_pending(voter_email, candidate_choice)
    if "Error" in message:
        flash(message, 'error')
    else:
        user_data['has_voted'] = True
        save_users(users)
        flash(message, 'info')

    return redirect(url_for('home'))


@app.route('/mine_block', methods=['GET'])  # Could be POST if preferred
def mine_block_route():
    if 'user_email' not in session:  # Optional: restrict who can mine
        flash('Please login to perform this action.', 'error')
        return redirect(url_for('login'))

    # Optional: check if user is admin
    # users = load_users()
    # if not users.get(session['user_email'], {}).get('is_admin', False):
    #     flash('You are not authorized to mine blocks.', 'error')
    #     return redirect(url_for('home'))

    message = blockchain.mine_pending_votes()
    flash(message, 'success' if "successfully" in message else 'info')
    return redirect(url_for('home'))


@app.route('/chain_data', methods=['GET'])
def get_chain_data():
    # Optional: Secure this endpoint if needed
    # if 'user_email' not in session:
    #     return jsonify({"error": "Unauthorized"}), 401

    response = {
        'chain': blockchain.get_chain_data_for_display(),
        'length': len(blockchain.chain),
        'is_valid': blockchain.is_chain_valid()
    }
    return jsonify(response)


@app.route('/current_results_json', methods=['GET'])
def current_results_json():
    # Optional: Secure this endpoint
    return jsonify(blockchain.get_results())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)