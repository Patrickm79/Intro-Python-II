# Write a class to hold player information, e.g. what room they are in
# currently.

from room import Room
from direction import Direction
from item import Item
from typing import List

class Player:

    def __init__(self, name: str, current_room: Room):
        self.name = name
        self.current_room = current_room
        self.inventory: List[Item] = []
        self.name = name
        self.current_room = current_room
        self.strength = 10
        self.defense = 2
        self.magic = 8  
        self.lvl = 1
        self.exp = 0 
        self.max_hp = 25
        self.stat = 0
        
    def can_move(self, direction: Direction):
        if direction == Direction.NORTH:
            return self.current_room.n_to is not None
        elif direction == Direction.SOUTH:
            return self.current_room.s_to is not None
        elif direction == Direction.EAST:
            return self.current_room.e_to is not None
        elif direction == Direction.WEST:
            return self.current_room.w_to is not None

    def move(self, direction: Direction):

        room_to = None

        if direction == Direction.NORTH:
            room_to = self.current_room.n_to
        elif direction == Direction.SOUTH:
            room_to = self.current_room.s_to
        elif direction == Direction.EAST:
            room_to = self.current_room.e_to
        elif direction == Direction.WEST:
            room_to = self.current_room.w_to

        if room_to is not None:
            self.current_room = room_to
        else:
            print("There is no room to move to in that direction!\n")

    def take(self, item: Item):
        self.current_room.items.remove(item)
        self.inventory.append(item)
        item.on_take()

    def drop(self, item: Item):
        self.inventory.remove(item)
        self.current_room.items.append(item)
        item.on_drop() 

        #
    def __str__(self):
        return f"{self.name} , {self.current_room}"  


    def try_movement(self,command):

        atribute = command + "_to"


        if hasattr(self.current_room, atribute):

            self.current_room = getattr(self.current_room, atribute)
            self.exp+=1

        else:
            print("you can't go that way!!")


    def lvl_up(self):
        base_exp = 10
        exp_multiplier = base_exp * self.lvl

        if self.exp >= exp_multiplier:
            self.lvl += 1
            self.max_hp += 10
            self.stats +=3

    def stats(self):
        return f'''
        level: {self.lvl}
        experience: {self.exp}
        strength: {self.strength}
        defense: {self.defense}
        magic: {self.magic}
        HP: {self.max_hp}
        available stat points: {self.stat}
        
        
        '''        
    def attack(self, monster):
        atk = monster.hp - self.strength
        monster.hp = atk