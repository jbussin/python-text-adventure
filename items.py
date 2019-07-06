"""Describes the items in the game."""
__author__ = 'Phillip Johnson'


class Item():
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
    

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)


class Weapon(Item):
    def __init__(self, name, description, value, damage, hp):
        self.damage = damage
        self.hp = hp
        super().__init__(name, description, value)
    
    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}\nPicked up: {}".format(self.name, self.description, self.value, self.damage, self.hp)


class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5,
                         hp=0)


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         damage=10,
                         hp = 1)


class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)
