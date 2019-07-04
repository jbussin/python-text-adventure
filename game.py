import world
from player import Player
 
def play():
    world.load_tiles()
    player = Player()
    while player.is_alive() and not player.victory:
        #Loop begins here

        class LeaveCaveRoom(MapTile):
            def intro_text(self):
                return """
                You see a bright light in the distance...
                ... it grows as you get closer! It's sunlight!
        
                Victory is yours!
                """
        
            def modify_player(self, player):
                player.victory = True
               
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
                    
if __name__ == "__main__":
    play()
