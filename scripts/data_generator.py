from game_player import Player
from game_villain import Villain
import pandas as pd
import random
import os

class BattleSimulations:
    def __init__(self):
        pass

    def _simulate_battle(self, player_class, villain_class):
        player_health_history = []
        villain_health_history = []
        player = player_class()
        villain = villain_class()

        player_health_history.append(player.health)
        villain_health_history.append(villain.health)

        max_turns = 100
        for turn in range(max_turns):
            if not player.is_alive() or not villain.is_alive():
                break

            player_action = random.choice(["attack", "dodge", "block"])
            villain_action = random.choice(["attack", "dodge", "block"])
            player_attack_index = random.randint(0, len(player.attacks) - 1) if player_action == "attack" else -1
            villain_attack_index = random.randint(0, len(villain.attacks) - 1) if villain_action == "attack" else -1
            player_damage = player.attack(player_attack_index) if player_action == "attack" else 0
            villain_damage = villain.attack(villain_attack_index) if villain_action == "attack" else 0

            # Handle Player's Actions
            if player_action == "dodge":
                if random.randint(0,10) < 2:
                    return True
                else:
                    return False
            
            elif player_action == "block":
                if villain_attack_index != -1 and villain.attacks[villain_attack_index]["blockable"]:
                    villain_damage = 0
                elif villain_attack_index != -1:
                    villain_damage //= 2

            # Handle Villain's Actions
            if villain_action == "dodge":
                if random.randint(0,10) < 2:
                    return True
                else:
                    return False
            elif villain_action == "block":
                if player_attack_index != -1 and player.attacks[player_attack_index]["blockable"]:
                    player_damage = 0
                elif player_attack_index != -1:
                    player_damage //= 2

            player.take_damage(villain_damage)
            villain.take_damage(player_damage)

            player_health_history.append(player.health)
            villain_health_history.append(villain.health)

        # Force a win/loss outcome if the loop finishes without a clear winner
        if player.is_alive() and villain.is_alive():
            # If both are still alive after max_turns, randomly decide the winner
            if random.choice([True, False]):
                outcome = 0  # Player Wins
            else:
                outcome = 1  # Villain Wins
        elif player.is_alive():
            outcome = 0  # Player Wins
        else:
            outcome = 1  # Villain Wins

        return player_health_history, villain_health_history, outcome


    def generate_training_data(self, player_class, villain_class, num_simulations, filename="training_data.csv"):
        all_player_health = []
        all_villain_health = []
        all_outcomes = []
        for _ in range(num_simulations):
            player_health, villain_health, outcome = self._simulate_battle(player_class, villain_class)
            all_player_health.append(player_health)
            all_villain_health.append(villain_health)
            all_outcomes.append(outcome)

        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)

        df = pd.DataFrame({
            'player_health_history': all_player_health,
            'villain_health_history': all_villain_health,
            'battle_outcome': all_outcomes
        })
        df.to_csv(filepath, index=False)
        print(f"Training data saved to {filepath}")

    def generate_test_data(self, player_class, villain_class, num_simulations, filename="test_data.csv"):
        all_player_health = []
        all_villain_health = []
        all_outcomes = []
        for _ in range(num_simulations):
            player_health, villain_health, outcome = self._simulate_battle(player_class, villain_class)
            all_player_health.append(player_health)
            all_villain_health.append(villain_health)
            all_outcomes.append(outcome)

        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)

        df = pd.DataFrame({
            'player_health_history': all_player_health,
            'villain_health_history': all_villain_health,
            'battle_outcome': all_outcomes
        })
        df.to_csv(filepath, index=False)
        print(f"Test data saved to {filepath}")

num_train_sims = 50
num_test_sims = 1000
battle_simulator = BattleSimulations()
battle_simulator.generate_training_data(Player, Villain, num_train_sims)
# battle_simulator.generate_test_data(Player, Villain, num_test_sims)