from abc import abstractmethod


class BasePlace:
    def __init__(self, location=None):
        if location is None:
            location = self.__class__.__name__
        self.location = location

    def get_location(self):
        return self.location

    @abstractmethod
    def get_antagonist(self):
        pass


class Place(BasePlace):
    def __init__(self, location=None):
        super(Place, self).__init__(location)

    def get_antagonist(self):
        print('Aliens  hid in craters')


class Kostroma(BasePlace):
    def __init__(self, location=None):
        super(Kostroma, self).__init__(location)

    def get_antagonist(self):
        print('Orcs hid in the forest')


class Tokyo(BasePlace):
    def __init__(self, location=None):
        super(Tokyo, self).__init__(location)

    def get_antagonist(self):
        print('Godzilla stands near a skyscraper')
