import time
from time import sleep


def retry(call_count, start_sleep_time, factor, boarder_sleep_time):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            start_t = time.perf_counter()
            i = 1
            t = start_sleep_time
            print(f'Кол-во запусков = {call_count}')
            print('Начало работы')
            while i != call_count + 1:
                t *= (2 ** factor)
                t = t if t < boarder_sleep_time else boarder_sleep_time
                sleep(t)
                result = func(i, *args, **kwargs)
                print(f'Запуск номер {i}. Ожидание {t} сек. Результат декорируемой функции = {result}')
                i += 1
            end_t = time.perf_counter()
            print('Конец работы')
            print('Время выполнения:', end_t - start_t, 'сек.')
            return result

        return wrapper

    return my_decorator


@retry(call_count=3, start_sleep_time=1, factor=2, boarder_sleep_time=20)
def func_result(i):
    if i < 3:
        return 'Нет соединения..'
    else:
        return 'Подключено!'


if __name__ == '__main__':
    func_result()
