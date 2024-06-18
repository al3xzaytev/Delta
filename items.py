# There are two types of items dropped after defeating a monster:
# 1. Consumables, which are used during a turn and give a buff for that turn.
# 2. Charms, which are used for the next battle.

class Items:
    def __init__(self, item_type):
        self.item_type = item_type

    class Consumable:
        def __init__(self, amount, usage):
            self.amount = amount
            self.usage = usage

    class Charm:
        def __init__(self, amount):
            self.amount = amount
