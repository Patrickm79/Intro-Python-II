from room import Room
from player import Player
from direction import Direction
from item import Item
import os
import time

# Declare all the rooms

room = {
    "outside":  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    "foyer":    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    "overlook": Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    "narrow":   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    "treasure": Room("Treasure Chamber", """You"ve found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link room together

room["outside"].n_to = room["foyer"]
room["foyer"].s_to = room["outside"]
room["foyer"].n_to = room["overlook"]
room["foyer"].e_to = room["narrow"]
room["overlook"].s_to = room["foyer"]
room["narrow"].w_to = room["foyer"]
room["narrow"].n_to = room["treasure"]
room["treasure"].s_to = room["narrow"]

# Add items

room["foyer"].items.append(Item("Flail", "A mace with a sharp ball attached by chain to the end."))
room["foyer"].items.append(Item("Gold", "100 gold coins"))
room["overlook"].items.append(Item("Quiver", "An empty quiver with a slightly magical hum."))
room["outside"].items.append(Item("Bow", "A sturdy compound bow made of a fine material."))

player_one = Player("Player One", room["outside"])


# Parsing

def parse_word(verb: str):
    verb = verb.lower()
    
    for direction in Direction:
        if verb == direction.value:
            if player_one.can_move(direction):
                player_one.move(direction)
                print_current_location(True)
            else:
                print("You can not move in that direction currently. Type m to see your map")
            return
    
    if verb == "q":
        print("Thanks for playing!")
        exit()
    elif verb == "i" or verb == "inventory":
        if len(player_one.inventory) > 0:
            print("Inventory:")
            for item in player_one.inventory:
                print(f"* {item.name}")
        else:
            print("You don't have any items in your inventory!")
    elif verb == "m" or verb == "map":
        display_map()
    else:
        print("""You must enter a valid command! 
Use "n", "s", "e", or "w" to navigate.
Use "i" to show your inventory. 
Type "q" to quit the game """)

def parse_words(verb: str, obj: str):
    verb = verb.lower()
    obj = obj.lower()

    if verb == "get" or verb == "take":
        for item in player_one.current_room.items:
            if obj == item.name.lower():
                player_one.take(item)
                return
        print("There are no items in the room by that name")
    elif verb == "drop":
        for item in player_one.inventory:
            if obj == item.name.lower():
                player_one.drop(item)
                return
        print("You don't have any items in your inventory by that name")
    else:
        print("You must enter a valid command! Accepted verbs are get, take, and drop")


# Printing

def print_slowly(string: str):
    string += "\n"
    for char in string:
        print(char, end="", flush=True)
        time.sleep(.04)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_current_location(animated: bool):
    clear_screen()
    print(f"{player_one.current_room.name}".center(50, "-") + "\n")
    if animated:
        print_slowly(player_one.current_room.description)
    else:
        print(player_one.current_room.description)

    if len(player_one.current_room.items) > 0:
        print("\n" + "VISIBLE ITEMS".center(50, "-") + "\n")
        for item in player_one.current_room.items:
            print(f"* {item.name}: {item.description}")

def display_map():
    clear_screen()
    
    nothing = "No visible path"
    north = player_one.current_room.n_to.name if player_one.current_room.n_to is not None else nothing
    south = player_one.current_room.s_to.name if player_one.current_room.s_to is not None else nothing
    west = player_one.current_room.w_to.name if player_one.current_room.w_to is not None else nothing
    east = player_one.current_room.e_to.name if player_one.current_room.e_to is not None else nothing

    print("Your Map".center(50, " "))
    print("".center(50, "="))

    print("\n" + north.center(50, " "))
    for _ in range(5):
        print("|".center(50, " "))
    print(west, end="")
    print("YOU".center(50 - len(west) - len(east), "-"), end="")
    print(east)
    for _ in range(5):
        print("|".center(50, " "))
    print(south.center(50, " "))

    print("\n" + "".center(50, "="))

    input("\nTap Return to Continue")
    print_current_location(False)

#
# Main
#

print_current_location(True)

while True:

    command = input("\nEnter a command: ")

    print("")

    words = command.split()
    
    if len(words) == 1:
        parse_word(words[0])
    elif len(words) == 2:
        parse_words(words[0], words[1])