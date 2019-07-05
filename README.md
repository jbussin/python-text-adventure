How to Write a Text Adventure in Python Part 1: Items and Enemies
This is an abbreviated version of the book Make Your Own Python Text Adventure.

Typically, a text adventure game involves the player exploring and interacting with a world to tell a story. For this tutorial, I wanted the game to take place in a cave with the goal of escaping alive. You can of course use this idea too, but feel free to use your own idea! Almost all parts of this tutorial are interchangeable with your own custom elements. We’re going to start by defining some items and enemies.

ITEMS
Start by creating a new directory called adventuretutorial and create a blank file called __init__.py. This tells the Python compiler that adventuretutorial is a Python package which contains modules. Go ahead and create your first module in this same directory called items.py.

The first class we are going to create is the Item class. When creating a class, consider the attributes that class should have. In general, it will be helpful for items to have a name and description. We can use these to give the player information about the item. Let’s also add a value attribute that will help players to compare items within an economy.

class Item():
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
 
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

This class has just two methods, but we’re going to see them pop up a lot. The __init__ method is the constructor and it is called whenever a new object is created. The __str__ method is usually a convenience for programmers as it allows us to print an object and see some useful information. Without a __str__ method, calling print() on an object will display something unhelpful like <__main__.Item object at 0x101f7d978>.


While we could create an Item directly, it wouldn’t be very interesting for the player because there is nothing special about it. Instead, we’re going to extend the Item class to define more specific items.


One of my favorite parts of games is finding treasure so let’s go ahead and create a Gold class.

class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)

The Gold class is now a subclass of the superclass Item. Another word for a subclass is child class and superclasses may be called parent or base classes.


The constructor here looks a little confusing but let’s break it down. First you’ll notice an additional parameter amt that defines the amount of this gold. Next, we call the superclass constructor using the super().__init__() syntax. The superclass constructor must always be called by a subclass constructor. If the constructors are exactly the same, Python will do it for us. However, if they are different, we have to explicitly call the superclass constructor. Note that this class doesn’t have a __str__ method. If a subclass doesn’t define its own __str__ method, the superclass method will be used in its place. That’s OK for the Gold class because the value is the same as the amount so there’s no reason to print out both attributes.


I mentioned earlier that this game is going to have weapons. We could extend Item again to make some weapons, but weapons all have something in general: damage. Whenever a lot of specific classes are going to share the same concept, it’s usually a good idea to store that shared concept in a superclass. To do this, we will extend Item into a Weapon class with a damage attribute and then extend Weapon to define some specific weapons in the game.


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)
 
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)
 
class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5)
 
class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         damage=10)

This should feel very familiar as we are following the same process of creating subclasses to define more specific elements in the game.


ENEMIES

Now that you’re an expert at extending objects, creating the enemies will be a breeze. Go ahead and create a new module called enemies.py.


Our base class Enemy should include a name, hit points, and damage the enemy does to the player. We’re also going to include a method that allows us to quickly check if the enemy is alive.

class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
 
    def is_alive(self):
        return self.hp &amp;gt; 0

Next, create a few subclasses of Enemy to define some specific enemies you want the player to encounter. Here are mine, but feel free to use your own ideas instead.


class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", hp=10, damage=2)
 
class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", hp=30, damage=15)

Notice that we don’t have to include is_alive() in the subclasses. This is because subclasses automatically get access to the methods in the superclass.


If you are completely new to programming, some of this may be confusing. My book Make Your Own Python Text Adventure is great for beginners because it does not assume any knowledge of programming concepts.


Click here for part 2

How to Write a Text Adventure in Python Part 2: The World Space
This is an abbreviated version of the book Make Your Own Python Text Adventure.

All games take place in some sort of world. The world can be as simple as a chess board or as complex as the Mass Effect universe and provides the foundation for the game as a whole. All elements of a game reside in the world and some elements interact with the world. In this post, you’ll learn how to add items and enemies to your world.

THE COORDINATE PLANE
A text adventure usually involves a player moving through the world one section per turn. We can think of each section as a tile on an x-y grid. Note: in most game programming the x-y coordinate plane is different from the one you learned in algebra. In the game world, (0,0) is in the top left corner, x increases to the right, and y increases to the bottom.

CREATING TILES
Start by creating a module tiles.py with this class:

import items, enemies
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

The import keyword means “give this module access the ‘items’ module and ‘enemies’ module. We need this because we will want to put these elements inside some of our rooms.


The MapTile class is going to provide a template for all of the tiles in our world, which means we need to define the methods that all tiles will need. First, we’ll want to display some text to the user when they enter the tile that describes the world. We also expect that some actions may take place when the player enters the tile, and that those actions change the state of the player (e.g., they pick something up, they win the game, something attacks them, etc.). Let’s add those methods now.



def intro_text(self):
    raise NotImplementedError()
 
def modify_player(self, player):
    raise NotImplementedError()

We haven’t talked about the code for the player yet, but that’s OK. The player parameter will serve as a placeholder. As you might guess, these methods aren’t going to do much in their current state. In fact, they will actually cause the program to crash! This might seem silly, but this behavior is to help us as programmers.


When thinking about our world, we don’t want to have tiles that do nothing. We may want tiles of water, tiles in a spaceship corridor, tiles with other characters, or tiles with treasure, but not empty tiles. So this MapTile class is actually just a template that all other tiles will expand on.


In the last post we learned about base classes. MapTile is actually a specific flavor of a base class. We call it an abstract base class because we don’t want to create any instances of it. In our game, we will only create specific types of tiles. We will never create a MapTile directly, instead we will create subclasses. The code raise NotImplementedError() will warn us if we accidentally create a MapTile directly.


Now on to our first tile subclass!


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself if a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

This class extends MapTile to make a more specific type of tile. We override the intro_text and modify_player methods to implement the specific behavior that this tile should have. A method is overridden when a subclass has the same method name as a superclass. Because it’s the starting room, I didn’t want anything to happen to the player. The pass keyword simply tells Python to not do anything. You might wonder why the method is even in this class if it doesn’t do anything. The reason is because if we don’t override modify_player, the superclass’s modify_player will execute and if that happens the program will crash because of raise NotImplementedError().


Next, let’s add a class for the tile where a player will find a new item.



class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)
 
    def add_loot(self, player):
        player.inventory.append(self.item)
 
    def modify_player(self, player):
        self.add_loot(player)

Remember, we haven’t created player yet, but we can guess that the player will have an inventory.


Let’s define one more type of room: a room in which the player encounters an enemy.




class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

This constructor should look familiar to you now. It’s very similar to the LootRoom constructor, but instead of an item, we are working with an enemy.


The logic for this room is a bit different. I didn’t want enemies to respawn. So if the player already visited this room and killed the enemy, they should not engage battle again. Assuming the enemy is alive, they attack the player and do damage to the player’s hit points.


Now that we have some basic types of tiles defined, we can make some even more specific versions. Here are some that I created:

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass
 
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """
 
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())
 
    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """

If you remember, I also created an Ogre enemy and Gold item. You may choose to create corresponding rooms too.


CREATING THE WORLD

We’re going to close out this post by actually creating a world based on the tiles we’ve defined. This delves into some advanced features so it’s OK if you don’t follow everything. I’ll explain everything briefly here, but I encourage you to read up on anything you’re interested in learning more about.


Create a new module in the same directory called world.py. Next, make a folder called “resources” that is in the same directory as the “adventuretotrial” directory and create map.txt inside. We’re going to build the world in this external file and load it into the game programatically.


I like to use a spreadsheet program and then copy the text into the map file, but you can just edit the file directly too. The goal is to lay out a grid of tiles whose names match the class names and are separated by tabs. Here’s an example in a spreadsheet:

Game tiles in spreadsheet


Remember, your map should not include MapTile, LootRoom, or EnemyRoom! Those are base classes that should not be created directly.


In the world module, add the following dictionary and method to parse the file you created.


_world = {}
starting_position = (0, 0)
 
def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
    x_max = len(rows[0].split('\t')) # Assumes all rows contain the same number of tabs
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '') # Windows users may need to replace '\r\n'
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)

The parsing method goes through each line of the file and splits the line into cells. Using a double for loop is a common way of working with grids. The x and y variables keep track of the coordinates. When we find the Starting Room, that position is saved because we will use it later. We use the global keyword to let us access the starting_position variable that lives outside of this method. The last line is the most interesting, but it’s fine if you don’t fully understand it.


The variable _world is a dictionary that maps a coordinate pair to a tile. So the code _world[(x, y)] creates the key (i.e. the coordinate pair) of the dictionary. If the cell is an empty string, we don’t want to store a tile in it’s place which is why we have the code None if tile_name == ''. However, if the cell does contain a name, we want to actually create a tile of that type. The getattr method is built into Python and lets us reflect into the tile module and find the class whose name matches tile_name. Finally the (x, y) passes the coordinates to the constructor of the tile.


Looking for an easier approach to building your world? Check out Chapter 13 of Make Your Own Python Text Adventure.


Essentially what we’re doing is using some advanced features in Python as an alternative to something like this:



tile_map = [[FindGoldRoom(),GiantSpiderRoom(),None,None,None],
            [None,StartingRoom(),EmptyCave(),EmptyCave(),None]
           ]

That’s hard to read and maintain. Using a text file makes changing our world easy. It’s also a lot simpler to visualize the world space.


Keep in mind that the only reason we are able to do this is because all of our tile classes derive from the same base class with a common constructor that accepts the parameters x and y.


Let’s add one more method to the world module that will make working with the tiles a little easier:



def tile_exists(x, y):
    return _world.get((x, y))

Congratulations for making it this far! If you’d like to see how to make the game easier or more difficult with different enemy types, see Chapter 12 of Make Your Own Python Text Adventure.



Click here for Part 3 of the abridged tutorial.

How to Write a Text Adventure in Python Part 3: Player Action
This is an abbreviated version of the book Make Your Own Python Text Adventure.

So far we’ve created a world and filled it with lots of interesting things. Now we’re going to create our player and provide ways for the player to interact with the world. This will probably be the most conceptually challenging part of the game, so you may want to re-read this section a few times.

THE PLAYER
Time for a new module! Create player.py and include this class:



import items
 
class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
 
    def is_alive(self):
        return self.hp &amp;gt; 0
 
    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

Now you can see some of the concepts that we previously templated have been made into reality. The player starts out with a few basic items and 100 hit points. We also load the starting location that was saved before and create a victory flag that will notify us if the player has won the game. The methods is_alive and print_inventory should be self-explanatory.


ADDING ACTIONS

Now that we have a player, we can start to give them actions. We’ll start with moving around first.


def move(self, dx, dy):
    self.location_x += dx
    self.location_y += dy
    print(world.tile_exists(self.location_x, self.location_y).intro_text())
 
def move_north(self):
    self.move(dx=0, dy=-1)
 
def move_south(self):
    self.move(dx=0, dy=1)
 
def move_east(self):
    self.move(dx=1, dy=0)
 
def move_west(self):
    self.move(dx=-1, dy=0)

The player can move in four directions: north, south, east, and west. To avoid repeating ourselves, we have a basic move method that takes care of actually changing the player’s position and then we have four convenience methods that use the common move method. Now we can simply refer to move_south without specifically trying to remember if y should be positive or negative, for example.


The next action the player should have is attack.

def attack(self, enemy):
    best_weapon = None
    max_dmg = 0
    for i in self.inventory:
        if isinstance(i, items.Weapon):
            if i.damage &amp;gt; max_dmg:
                max_dmg = i.damage
                best_weapon = i
 
    print("You use {} against {}!".format(best_weapon.name, enemy.name))
    enemy.hp -= best_weapon.damage
    if not enemy.is_alive():
        print("You killed {}!".format(enemy.name))
    else:
        print("{} HP is {}.".format(enemy.name, enemy.hp))

In order to find the most powerful weapon in the player’s inventory, we loop through all the items and use isinstance (a built-in function) to see if the item is a Weapon. This is another feature we gain by having all of our weapons share a common class. If we didn’t do this, we would need to do something messy like if item.name=="dagger" or item.name=="rock" or item.name=="sword".... The rest of the method actually attacks the enemy and reports the result back to the user.


We now have behavior defined for certain actions. But within the game, we need some additional information. First, we need to bind keyboard keys to these actions. It would also be nice if we had a “pretty” name for each action that could be displayed to the player. Because of this additional “meta” information, we are going to wrap these behavior methods inside of classes. It’s time for a new module called actions.py


import Player
 
class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs
 
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)

We’re going to use the now-comfortable design of a base class with specific subclasses. For starters, the Action class will have a method assigned to it. This method will correspond directly to one of the action methods in the player class, which you will see shortly. Additionally, each Action will have a hotkey, the “pretty” name, and a slot for additional parameters. These additional parameters are specified by the special ** operator and are named kwargs by convention. Using **kwargs allows us to make the Action class extremely flexible. We know all actions will require certain parameters, but there may be additional parameters that are different for certain actions. For example, we’ve already seen the attack method that requires an enemy parameter.


The following classes are our first wrappers:

class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move north', hotkey='n')
 
class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move south', hotkey='s')
 
class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move east', hotkey='e')
 
class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move west', hotkey='w')
 
class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey='i')

Notice how the method parameter actually points to a specific method in the Player class. Referring to methods as objects in a feature in Python and other languages with “first class” methods. Be sure that you do not include () after the method name. The code Player.some_method() will execute the method whereas Player.some_method is just a reference to the method as an object.


The attack method wrapper is very similar with one small difference:



class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='a', enemy=enemy)

Here we have included the “enemy” parameter as previously discussed. Since enemy is not a named parameter in the base Action class constructor, it will get bundled up into the **kwargs parameter.


Now that we have some actions defined, we need to consider how they will be used in the game. For example, the player should not be able to attack when no enemy is present. Conversely, they shouldn’t be able to calmly leave a room that has an enemy! Actions should be available or unavailable based on the context of the situation. To handle this, we need to flip back to our tiles module.


Change your import statement to include the actions and world modules:


1
import items, enemies, actions, world

Next add the following methods to MapTile:


def adjacent_moves(self):
    """Returns all move actions for adjacent tiles."""
    moves = []
    if world.tile_exists(self.x + 1, self.y):
        moves.append(actions.MoveEast())
    if world.tile_exists(self.x - 1, self.y):
        moves.append(actions.MoveWest())
    if world.tile_exists(self.x, self.y - 1):
        moves.append(actions.MoveNorth())
    if world.tile_exists(self.x, self.y + 1):
        moves.append(actions.MoveSouth())
    return moves
 
def available_actions(self):
    """Returns all of the available actions in this room."""
    moves = self.adjacent_moves()
    moves.append(actions.ViewInventory())
 
    return moves

These methods provide some default behavior for a tile. The default actions that a player should have are: move to any adjacent tile and view inventory. The method adjacent_moves determines which moves are possible in the map. For each available action, we append an instance of one of our wrapper classes to the list. Since we used the wrapper classes, we will later have easy access to the names and hotkeys of the actions.


Now we need to allow the Player class to take an Action and run the action’s internally-bound method. Add this method to the Player class:


def do_action(self, action, **kwargs):
    action_method = getattr(self, action.method.__name__)
    if action_method:
        action_method(**kwargs)

That getattr rears its head again! We have a similar concept to what we did to create tiles, but this time instead of looking for a class in a module, we’re looking for a method in a class. For example, if action is a MoveNorth action, then we know that its internal method is Player.move_north. The __name__ of that method is “move_north”. Then getattr finds the move_north method inside the Player class and stores that method as the object action_method. If getattr was successful, we execute the found method and we include the **kwargs in case that method needs additional objects (like the attack method).


Looking for something a little simpler? My book Make Your Own Python Text Adventure has a different approach to player actions that avoids the sometimes confusing getattr and **kwargs.


At this point, I decided to add one more action: flee. As an alternative to battle, the player can flee which causes them to a random adjacent tile. Here’s the behavior for the Player in the players module:


import random #Note the new import!
import items, world
 
class Player:
    # Existing code omitted for brevity
 
    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

And here’s our wrapper in the actions module:


class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)

Similar to the attack action, the flee action requires an additional parameter. This time, it’s the tile from which the player needs to flee.


Most of the tiles we have created so far can use the default available moves. However, the enemy tiles need to provide the attack and flee actions. To do this, we will override the default behavior of the MapTile class with our own version of the method in the EnemyRoom class.


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
 
    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

If the enemy is still alive then the player’s only options are attack or flee. If the enemy is dead, then this room works like all other rooms.


Whew! That was a lot of new code. We’re almost finished! All we need to do to wrap up is create and interface for the human player.


Click here for part 4

How to Write a Text Adventure in Python Part 4: The Game Loop
This is an abbreviated version of the book Make Your Own Python Text Adventure.

The end is near, we’re almost ready to play the game! We’ll finish this series by implementing the game loop and receiving input from the human player.

THE GAME LOOP
While some applications follow a discrete set of steps and terminate, a game typically just “keeps going”. The only way the program stops is if the player wins, loses, or quits. To handle this behavior, games usually run inside a loop. On each iteration, the game state is updated and input is received from the human player. In graphical games, the loop runs many times per second. Since we don’t need to continually refresh the player’s screen for a text game, our code will actually pause until the player provides input. Our game loop is going to reside in a new module game.py.

import world
from player import Player
 
def play():
    world.load_tiles()
    player = Player()
    while player.is_alive() and not player.victory:
        #Loop begins here

Before play begins, we load our world from the text file and create a new Player object. Next, we begin the loop. Note the two conditions we check: if the player is alive and if victory has not been achieved. For this game, the only way to lose is by dying. However, there isn’t any code yet that lets the player win. In my story, I want the player to escape the cave alive. If they do that, they win. To implement this behavior, we’re going to add a very simple room and place it into our world. Switch back to tiles.py and add this class:

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True

Don’t forget to include one of these rooms somewhere in your map.txt file. Now that the player can win, let’s finish the game loop.

def play():
    world.load_tiles()
    player = Player()
    #These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break

The first thing the loop does is find out what room the player is in and then executes the behavior for that room. If the player is alive and they have not won after the behavior executes, we prompt the human player for input. This is done using the built-in input() function. If the human player provided a matching hotkey, then we execute the associated action using the do_action method.


The last thing we need to include is an instruction for Python to know that play() should run when running the file. Include these lines at the bottom of the game.py module:


if __name__ == "__main__":
    play()

To run the program, navigate to the folder containing the adventuretutorial package in your console and run python adventuretutorial/game.py. If you get warnings about packages, try setting your PYTHONPATH environment variable manually. Have fun!


WHERE TO GO FROM HERE

Congratulations! You now have a working text adventure game. With the information learned here, you should be able to quickly add your own custom items, enemies, and tiles. If you’re up for more of a challenge, here are some of the features included in Make Your Own Python Text Adventure:



An easier and more flexible way to build your world (no text files or reflection!)

A game economy where the player can buy and sell items

The ability for players to heal during and between fights

Difficulty settings to make the game harder or easier

