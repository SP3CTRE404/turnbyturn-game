from game_player import Player
from game_villain import Villain
import pandas as pd
import random
import os

class DataGenerator:
    def __init__(self):
        pass

    def _simulate_battle(self, player_class, villain_class, max_turns):
        player_health_history = []
        villain_health_history = []
        player = player_class()
        villain = villain_class()

        player_health_history.append(player.health)
        villain_health_history.append(villain.health)

        battle_finished = False
        for turn in range(max_turns):
            if not player.is_alive() or not villain.is_alive():
                battle_finished = True
                break

            player_action = random.choice(["attack", "dodge", "block"])
            villain_action = random.choice(["attack", "dodge", "block"])
            player_attack_index = random.randint(0, len(player.attacks) - 1) if player_action == "attack" else -1
            villain_attack_index = random.randint(0, len(villain.attacks) - 1) if villain_action == "attack" else -1
            player_damage = player.attack(player_attack_index) if player_action == "attack" else 0
            villain_damage = villain.attack(villain_attack_index) if villain_action == "attack" else 0

            # Handle Player's Actions
            if player_action == "dodge":
                if random.random() < 0.2:  # 20% chance to dodge
                    villain_damage = 0
            elif player_action == "block":
                if villain_attack_index != -1 and villain.attacks[villain_attack_index]["blockable"]:
                    villain_damage = 0
                elif villain_attack_index != -1:
                    villain_damage //= 2

            # Handle Villain's Actions
            if villain_action == "dodge":
                if random.random() < 0.2:  # 20% chance to dodge
                    player_damage = 0
            elif villain_action == "block":
                if player_attack_index != -1 and player.attacks[player_attack_index]["blockable"]:
                    player_damage = 0
                elif player_attack_index != -1:
                    player_damage //= 2

            player.take_damage(villain_damage)
            villain.take_damage(player_damage)

            player_health_history.append(player.health)
            villain_health_history.append(villain.health)

        outcome = -1  # Indicate inconclusive battle if max turns reached without a winner
        if not battle_finished:
            if player.is_alive() and villain.is_alive():
                outcome = -1 # Still inconclusive
            elif player.is_alive():
                outcome = 0  # Player Wins (shouldn't happen if battle_finished is False)
            else:
                outcome = 1  # Villain Wins (shouldn't happen if battle_finished is False)
        else:
            if player.is_alive() and not villain.is_alive():
                outcome = 0  # Player Wins
            elif not player.is_alive() and villain.is_alive():
                outcome = 1  # Villain Wins

        return player_health_history, villain_health_history, outcome, battle_finished


    def generate_training_data(self, player_class, villain_class, num_simulations, filename="training_data.csv"):
        all_player_health = []
        all_villain_health = []
        all_outcomes = []
        excluded_inconclusive_count = 0
        for _ in range(num_simulations):
            player_health, villain_health, outcome, wont_need = self._simulate_battle(player_class, villain_class, 100)
            if outcome != -1:
                all_player_health.append(player_health)
                all_villain_health.append(villain_health)
                all_outcomes.append(outcome)
            else:
                excluded_inconclusive_count += 1

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
        print(f"Number of inconclusive battles excluded from training: {excluded_inconclusive_count}")

    def generate_test_data(self, player_class, villain_class, num_simulations, filename="test_data.csv"):
        all_player_health = []
        all_villain_health = []
        all_outcomes = []
        excluded_finished_early_count = 0
        for _ in range(num_simulations):
            player_health, villain_health, outcome, battle_finished = self._simulate_battle(player_class, villain_class, 10)
            if not battle_finished:
                all_player_health.append(player_health)
                all_villain_health.append(villain_health)
                all_outcomes.append(outcome)
            else:
                excluded_finished_early_count += 1

        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)

        df = pd.DataFrame({
            'player_health_history': all_player_health,
            'villain_health_history': all_villain_health,
            # 'battle_outcome': all_outcomes
        })
        df.to_csv(filepath, index=False)
        print(f"Test data saved to {filepath}")
        print(f"Number of battles excluded from testing (finished within 10 turns): {excluded_finished_early_count}")

    def generate_eval_data(self, player_class, villain_class, num_eval_simulations, filename="eval_data.csv"):
        all_player_health = []
        all_villain_health = []
        all_outcomes = []
        excluded_inconclusive_count = 0

        for _ in range(num_eval_simulations):  
            player_health, villain_health, outcome, wont_need = self._simulate_battle(player_class, villain_class, 100)

            if outcome != -1 and len(player_health) >= 5 and len(villain_health) >= 5:
                all_player_health.append(player_health[:10])  # Store only first 5 turns
                all_villain_health.append(villain_health[:10])  # Store only first 5 turns
                all_outcomes.append(outcome)
            else:
                excluded_inconclusive_count += 1

        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)

        df = pd.DataFrame({
            'player_health_history': all_player_health,
            'villain_health_history': all_villain_health,
            'battle_outcome': all_outcomes
        })
        df.to_csv(filepath, index=False)

        print(f"Evaluation data saved to {filepath} (first {num_eval_simulations} complete simulations that lasted at least 5 turns)")
        print(f"Number of battles excluded from evaluation (inconclusive or less than 5 turns): {excluded_inconclusive_count}")


num_train_sims = 50000
num_eval_sims = 1000
num_test_sims = 100
battle_simulator = DataGenerator()
# battle_simulator.generate_training_data(Player, Villain, num_train_sims)
battle_simulator.generate_test_data(Player, Villain, num_test_sims)
# battle_simulator.generate_eval_data(Player, Villain, num_eval_sims)