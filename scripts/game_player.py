import random

class Player:
    def __init__(self, name="Player", health=100):
        self.name = name
        self.health = health
        self.attacks = {
            0: {"name": "Quick Strike", "damage": 8, "blockable": True},
            1: {"name": "Strong Strike", "damage": 20, "blockable": True},
            2: {"name": "Fireball", "damage": 16, "blockable": False},
            3: {"name": "Ice Shard", "damage": 12, "blockable": True},
            4: {"name": "Poison Dart", "damage": 20, "blockable": True}
        }

    def attack(self, attack_index):
        if attack_index in self.attacks:
            return self.attacks[attack_index]["damage"]
        else:
            return 0  # Invalid attack index

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(0, self.health)

    def dodge(self):
        return random.choice([True, False])

    def block(self, incoming_attack_index, villain_attacks):
        if incoming_attack_index in villain_attacks and villain_attacks[incoming_attack_index]["blockable"]:
            return villain_attacks[incoming_attack_index]["damage"] // 2
        elif incoming_attack_index in villain_attacks:
            return villain_attacks[incoming_attack_index]["damage"]
        else:
            return 0

    def is_alive(self):
        return self.health > 0
