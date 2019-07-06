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
    def __init__(self, name, description, value, damage, on_floor):
        self.damage = damage
        self.on_floor = on_floor
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}\non Floor?: {}".format(self.name, self.description, self.value, self.damage, self.on_floor)


class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5,
                         on_floor='no')


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         damage=10,
                         on_floor = 'yes')


class Gold(Weapon):
    def __init__(self, amt, on_floor):
        self.amt = amt
        self.on_floor = on_floor
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt,
                         damage = 0,
                         on_floor = self.on_floor)
