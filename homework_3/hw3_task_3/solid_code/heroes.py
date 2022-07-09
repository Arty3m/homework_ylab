from abc import abstractmethod
from antagonistfinder import AntagonistFinder


class BaseAttack:
    def attack(self):
        print('PUNCH')


class GunAttack:
    def fire_a_gun(self):
        print('PIU PIU')


@abstractmethod
class UltimateAttack:
    def ultimate(self):
        pass


class SuperHero(BaseAttack):

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)


class Superman(UltimateAttack, SuperHero):

    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def attack(self):
        print('KICK')

    def ultimate(self):
        print('Wzzzuuuup!')


class ChackNorris(GunAttack, SuperHero):
    def __init__(self):
        super(ChackNorris, self).__init__('Chack Noris', False)

    def attack(self):
        self.fire_a_gun()
