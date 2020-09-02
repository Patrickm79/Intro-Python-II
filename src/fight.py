def fight(monster,player):
    while True:
        action = input('A monster has appeared!! Fight or flee?')

        if action == 'fight':
            monster.attack(player)
            print(f'The monster has attacked! Remaining hp:{player.max_hp}')
            player.attack(monster)
            print(f' Your attack hits! Remaining monster hp:{monster.hp}')

        if action == 'flee':
            break

        if monster.hp == 0:
            print('You have defeated the monster!')
            break