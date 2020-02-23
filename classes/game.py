import random
import pprint
from classes.magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def generate_spell_damage(self, i):
        mgl = self.magic[i]["dmg"] - 5
        mgh = self.magic[i]["dmg"] + 5
        return random.randrange(mgl, mgh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\tACTIONS" + bcolors.ENDC)
        for item in self.action:
            print("\t\t" + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\tMAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("\t\t" + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\tITEMS" + bcolors.ENDC)
        for item in self.items:
            print("\t\t" + str(i) + ":", item["item"].name, ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print(bcolors.FAIL + bcolors.BOLD + "\tTARGET" + bcolors.ENDC)
        for enemy in enemies:
            print("\t\t" + str(i) + "." + enemy.name)
            i += 1
        choice = int(input("\tChoose target:")) - 1
        return choice

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_damage = spell.generate_damage()
        return spell, magic_damage

    def get_enemy_stats(self):

        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_bar = bcolors.FAIL + hp_bar + bcolors.ENDC

        chp = str(self.hp) + "/" + str(self.maxhp)
        while len(chp) + len(self.name) < 24:
            chp = " " + chp

        print("                           __________________________________________________")
        print(bcolors.BOLD + self.name + ":" + chp + " |" + hp_bar + "|")

    def get_stats(self):

        hp_bar = ""
        mp_bar = ""

        # Generate HP Bar
        bar_ticks = (self.hp / self.maxhp) * 100 / 4
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "
        if self.hp / self.maxhp < 1 / 3:
            hp_bar = bcolors.FAIL + hp_bar + bcolors.ENDC
        else:
            hp_bar = bcolors.OKGREEN + hp_bar + bcolors.ENDC

            # Generate MP Bar
        bar_ticks = (self.mp / self.maxmp) * 100 / 10
        while bar_ticks > 0:
            mp_bar += "█"
            bar_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        chp = str(self.hp) + "/" + str(self.maxhp)
        while len(chp) + len(self.name) < 24:
            chp = " " + chp

        cmp = str(self.mp) + "/" + str(self.maxmp)
        while len(cmp) < 11:
            cmp = " " + cmp

        print("                           _________________________              __________ ")
        print(bcolors.BOLD + self.name + ":" +
              chp + " |" + hp_bar +
              "|" +
              cmp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")
