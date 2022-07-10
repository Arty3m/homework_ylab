import redis
import time


def cacher(func):
    """Декоратор, который кэширует данные в redis, при повторном запросе возвращает из кэша"""

    def wrapper(num: int, *args, **kwargs):
        redis_client = redis.Redis('localhost')
        cache = redis_client.get(str(num))
        if cache is not None:
            redis_client.close()
            return int(cache)

        result = func(num, *args, **kwargs)

        redis_client.set(str(num), str(result))
        redis_client.close()

        return result

    return wrapper


@cacher
def multiplier(number: int):
    time.sleep(3)
    return number * 2


if __name__ == '__main__':
    numbers = (2, 2, 3, 3, 5, 5)
    for el in numbers:
        start_t = time.perf_counter()

        print('Результат вычислений:', multiplier(el))

        end_t = time.perf_counter()
        print('Выполнилось за: ', end_t - start_t, 'сек.')
