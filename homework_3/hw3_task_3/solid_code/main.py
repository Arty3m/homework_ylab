from typing import Union
from heroes import Superman, ChackNorris, SuperHero
from places import Kostroma, Tokyo, Place, BasePlace


class MassMedia:
    def create_news(self, name: SuperHero, place: BasePlace, source: str):
        place_name = place.get_location()
        print(f'{source}: {name} saved the {place_name}!')


def save_the_place(hero: SuperHero, place: BasePlace, media: MassMedia):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    media.create_news(hero.name, place, 'TV')


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma(), MassMedia())
    print('-' * 20)
    save_the_place(ChackNorris(), Tokyo(), MassMedia())
    # print('-' * 20)
    # save_the_place(Superman(), Place([123498.5125, 9870415.6]), MassMedia())
#
