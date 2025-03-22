# Turn-Based Game with Counter-Move Prediction

This project implements a turn-based battle game with an LSTM model for predicting counter-moves based on damage patterns.

## Overview

The game simulates battles between a Player and a Villain, where each character has a set of attacks, dodge, and block mechanics. The game utilizes an LSTM neural network to predict the optimal counter-move based on the damage dealt in previous turns.

## Features

* **Player and Villain Classes:**
    * Characters with health, attacks, dodge, and block capabilities.
    * Attacks deal damage as multiples of 4.
    * Villain has special attacks that are partially blocked.
* **Data Generation:**
    * Simulates battles to generate training data.
    * Data includes turn number, player damage, villain damage, and optimal counter-move.
* **LSTM Model:**
    * Predicts counter-moves based on previous turn damage patterns.
    * Trained using PyTorch.
* **Game Logic:**
    * Applies predicted counter-moves to modify damage dealt.
    * Turn-based battle simulation.

## Project Structure
Turn_based_game/
├── data/
│   └── battle_data.parquet
├── models/
│   └── counter_move_model.pth
├── scripts/
│   ├── data_generator.py
│   ├── game_logic.py
│   ├── model.py
│   ├── predict.py
│   └── train.py
├── README.md
└── .gitignore

* `data/`: Contains the generated battle data.
* `models/`: Stores the trained LSTM model.
* `scripts/`: Contains the Python scripts for data generation, model training, and game logic.
    * `data_generator.py`: Generates the training dataset.
    * `model.py`: Defines the LSTM model architecture.
    * `train.py`: Trains the LSTM model.
    * `predict.py`: Predicts counter-moves using the trained model.
    * `game_logic.py`: Implements the game's turn-based logic.
* `README.md`: This file.
* `.gitignore`: Specifies files and directories to ignore in Git.

## Requirements

* Python 3.x
* PyTorch
* Pandas
* Parquet

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/SP3CTRE404/Turn_based_game.git](https://github.com/SP3CTRE404/Turn_based_game.git)
    cd Turn_based_game
    ```

2.  **Install the required packages:**

    ```bash
    pip install torch pandas pyarrow
    ```

## Usage

1.  **Generate the training dataset:**

    ```bash
    python scripts/data_generator.py
    ```

2.  **Train the LSTM model:**

    ```bash
    python scripts/train.py
    ```

3.  **Run the game logic (example):**

    * You will need to implement the game loop and use the predict function from `predict.py` within your game logic.

    ```python
    #example usage.
    from scripts.predict import predict_counter_move
    from scripts.model import LSTMModel
    import torch

    #load model.
    input_size = 2
    hidden_size = 128
    output_size = 3
    model = LSTMModel(input_size, hidden_size, output_size)
    model.load_state_dict(torch.load('models/counter_move_model.pth'))

    #generate input sequence.
    input_sequence = torch.tensor([[10, 5], [12, 8], [20, 4], [8, 16], [16, 12]], dtype=torch.float32)

    #predict the counter move.
    predicted_move = predict_counter_move(model, input_sequence)

    print(f"Predicted Counter Move: {predicted_move}")

    #Use the predicted move within your game logic.
    ```

## Notes

* This is a basic implementation and can be extended with more features, such as character classes, items, and more complex game mechanics.
* The LSTM model's performance can be improved by tuning hyperparameters and using more extensive training data.
* Game logic needs to be implemented.