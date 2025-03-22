
class Villain:
    def __init__(self, name="Villain", health=100):
        self.name = name
        self.health = health
        self.attacks = {
            0: {"name": "Claw Swipe", "damage": 12, "blockable": True},
            1: {"name": "Bite", "damage": 16, "blockable": True},
            2: {"name": "Heavy Smash", "damage": 24, "blockable": True},
            3: {"name": "Fire Breath", "damage": 20, "blockable": False},
            4: {"name": "Poison Spit", "damage": 16, "blockable": True},
            5: {"name": "Special 1", "damage": 20, "blockable": True},
            6: {"name": "Special 2", "damage": 24, "blockable": True},
            7: {"name": "Special 3", "damage": 28, "blockable": True}
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

    def block(self, incoming_attack_index, player_attacks):
        if incoming_attack_index in player_attacks and player_attacks[incoming_attack_index]["blockable"]:
            return player_attacks[incoming_attack_index]["damage"] // 2
        elif incoming_attack_index in player_attacks:
            return player_attacks[incoming_attack_index]["damage"]
        else:
            return 0

    def is_alive(self):
        return self.health > 0