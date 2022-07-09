from typing import Union
from heroes import Superman, ChackNorris, SuperHero
from places import Kostroma, Tokyo


class MassMedia:
    def create_news(self, name: str, place, source: str):
        place_name = getattr(place, 'name', place)
        print(f'{source}: {name} saved the {place_name}!')


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo], media: MassMedia):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    media.create_news(hero.name, place, 'TV')


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma(), MassMedia())
    print('-' * 20)
    save_the_place(ChackNorris(), Tokyo(), MassMedia())
