from itertools import cycle


class Range2:
    def __init__(self, stop_value: int):
        self.current = -1
        self.stop_value = stop_value - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop_value:
            self.current += 1
            return self.current
        raise StopIteration


class CyclicIterator:
    def __init__(self, iterable_obj):
        self._collection = cycle(iter(iterable_obj))

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._collection)


if __name__ == '__main__':

    cyclic_iterator = CyclicIterator(range(3))
    # cyclic_iterator = CyclicIterator('ssd')
    # cyclic_iterator = CyclicIterator([1, 2, 5, 6, 7])
    # cyclic_iterator = CyclicIterator((3, 5, 8, 7))
    # cyclic_iterator = CyclicIterator({1, 2, 3, 4})
    # cyclic_iterator = CyclicIterator(Range2(5))

    for i in cyclic_iterator:
        print(i)
