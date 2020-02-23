import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 160, "Black")
ice = Spell("Ice", 15, 180, "Black")
thunder = Spell("Thunder", 20, 200, "Black")
storm = Spell("Storm", 15, 170, "Black")

# Create White Magic
cure = Spell("Cure", 12, 120, "White")
healing = Spell("healing", 20, 250, "White")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, ice, storm, cure, healing]
enemy_magic = [fire, thunder, storm]

player_items = [{"item": potion, "quantity": 1}, {"item": elixir, "quantity": 5},
                {"item": grenade, "quantity": 5}, {"item": hielixir, "quantity": 1}]

# Instantiate People
player1 = Person("Dylan", 500, 100, 60, 34, player_magic, player_items)
player2 = Person("Carlos", 500, 10000, 60, 34, player_magic, player_items)
player3 = Person("Mikey", 500, 100, 60, 34, player_magic, player_items)

enemy1 = Person("BOSS", 2000, 100, 100, 20, enemy_magic, [])
enemy2 = Person("EMP 1", 700, 100, 60, 20, enemy_magic, [])
enemy3 = Person("EMP 2", 700, 100, 60, 20, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("========================")

    for player in players:
        player.get_stats()

    print("________________________")
    for enemy in enemies:
        enemy.get_enemy_stats()

    # Players attack phase
    for player in players:
        if player.get_hp() == 0:
            continue

        print("\t" + bcolors.BOLD + player.name + bcolors.ENDC)
        player.choose_action()
        choice = input("\tChoose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + " for ", dmg, "points of damage. Enemy HP:",
                  enemies[enemy].get_hp())

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            enemy = player.choose_target(enemies)

            player.choose_magic()
            magic_choice = int(input("\tChoose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if current_mp < spell.cost:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "Black":
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg),
                      "points of damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] <= 0:
                print(bcolors.FAIL + "\nNone left\n" + bcolors.ENDC)
                continue
            else:
                player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP")
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for member in players:
                        member.hp = member.maxhp
                        member.mp = member.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # Enemies attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        target = random.randrange(0, 3)
        if players[target].get_hp() == 0:
            target = (target + 1) % 3
        if enemy_choice == 0:
            # Enemy attack
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name + " attacked " + players[target].name + " for " + bcolors.FAIL + str(
                enemy_dmg) + bcolors.ENDC + " damage.")
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            players[target].take_damage(magic_dmg)
            print(
                enemy.name + " used " + spell.name + " deals " + bcolors.FAIL + str(magic_dmg) + bcolors.ENDC + " to " +
                players[target].name)

    # Check if battle is over
    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Players won
    if len(enemies) == 0:
        print(bcolors.OKGREEN + " YOU WIN !" + bcolors.ENDC)
        running = False

    # Check if Enemies won
    elif defeated_players == len(players):
        print(bcolors.FAIL + "You has been defeated!" + bcolors.ENDC)
        running = False
