#this is enemies

class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
 
    def is_alive(self):
        return self.hp &amp;gt; 0

class Beefo(Enemy):
    def __init__(self):
        super().__init__(name="Beefaroni", hp=10, damage=2)
 
class BigJim(Enemy):
    def __init__(self):
        super().__init__(name="Big Jim", hp=30, damage=15)