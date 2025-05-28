# Blockchain Voting System MVP

A simple, Dockerized web application demonstrating a blockchain-based voting system. Built with Python (Flask) for the backend and a custom blockchain implementation, and styled with Tailwind CSS & daisyUI for the frontend. This project was developed as a university MVP.

## Features

* **User Authentication:** Secure user registration and login using hashed passwords. User data is stored in a local `users.json` file.
* **Voting Mechanism:**
    * Registered and logged-in users can cast a single vote for predefined candidates.
    * Votes are collected as pending transactions before being added to the blockchain.
* **Blockchain Core:**
    * Custom-built blockchain logic in Python.
    * Blocks include index, timestamp, data (votes), previous hash, nonce, and its own hash.
    * Simplified Proof-of-Work for mining new blocks.
* **Block Mining:** A manual trigger allows pending votes to be "mined" into a new block and added to the chain.
* **Transparent Results:** View real-time vote counts for each candidate.
* **Blockchain Explorer:** An endpoint (`/chain_data`) provides a JSON representation of the entire blockchain for transparency and inspection.
* **Responsive Frontend:** User interface built with HTML, Tailwind CSS, and daisyUI (via CDNs) for a clean and modern look.
* **Dockerized:** Fully containerized for easy setup and execution using Docker Compose.

## Technologies Used

* **Backend:** Python 3.10, Flask
* **Password Hashing:** Werkzeug
* **Frontend:** HTML, Tailwind CSS (CDN), daisyUI (CDN)
* **Blockchain:** Custom Python implementation
* **Data Storage:**
    * `users.json` for user credentials and voting status.
    * Blockchain and candidate data are currently in-memory (reset on application restart).
* **Containerization:** Docker, Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed:
* Docker Desktop (which includes Docker Engine and Docker Compose)

## Project Setup & Installation

1.  **Clone the Repository (Example):**
    ```bash
    git clone <your-repository-url>
    cd blockchain_voting_mvp_flask
    ```
    (If you don't have a Git repository yet, simply ensure all project files are in a directory named `blockchain_voting_mvp_flask` or similar.)

2.  **Ensure `users.json` exists:**
    Before running the application for the first time, create an empty `users.json` file in the root of the project directory:
    ```bash
    echo "{}" > users.json
    ```
    This file will store registered user data.

## Running the Project

The recommended way to run this project is using Docker Compose.

1.  **Navigate to the project root directory** (e.g., `blockchain-voting-app-master`) in your terminal.

2.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    * The `--build` flag ensures Docker images are built (or rebuilt if there are changes).
    * This command will start the Flask application inside a Docker container.

3.  **Access the Application:**
    Once the container is running (you'll see logs from the Flask development server in your terminal, typically indicating it's running on `http://0.0.0.0:5000/`), open your web browser and go to:
    [http://localhost:5000](http://localhost:5000)

## How to Use

1.  **Register:** If you are a new user, click on "Register" in the navbar and create an account with your email and a password.
2.  **Login:** Use your registered credentials to log in.
3.  **Vote:**
    * Once logged in, you'll see the main voting page.
    * Select a candidate from the dropdown list.
    * Click "Submit Vote". You can only vote once.
4.  **Mine Blocks:**
    * After votes have been submitted, they are "pending".
    * Click the "Mine Pending Votes" button (the count of pending votes will be displayed). This action will bundle pending votes into a new block, perform a simplified Proof-of-Work, and add the block to the chain.
    * Vote counts in the "Live Results" section will update after mining.
5.  **View Results:** The "Live Results" section on the main page shows the current tally for each candidate based on votes in mined blocks.
6.  **View Blockchain:** Click the "View Blockchain (JSON)" link (usually on the main page) to open a new tab displaying the raw JSON data of the entire blockchain, including all blocks and their contents.

## Stopping the Application

* To stop the Dockerized application, go to the terminal where `docker-compose up` is running and press `Ctrl+C`.
* To remove the containers (optional, if you want to clean up):
    ```bash
    docker-compose down
    ```

## Project Structure