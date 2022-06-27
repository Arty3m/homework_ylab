import itertools
import re
from ipaddress import IPv4Address
import math


def domain_name(url):
    return re.match(r'(https?:\/\/)?(www.)?(\w+-?\w+)\.(\w+)', url)[3]


assert domain_name("http://github.com/carbonfive/raygun") == "github"
assert domain_name("http://www.zombie-bites.com") == "zombie-bites"
assert domain_name("https://www.cnet.com") == "cnet"
assert domain_name("http://google.com") == "google"
assert domain_name("http://google.co.jp") == "google"
assert domain_name("www.xakep.ru") == "xakep"
assert domain_name("https://youtube.com") == "youtube"


def int32_to_ip(int32):
    return str(IPv4Address(int32))


assert int32_to_ip(2154959208) == "128.114.17.104"
assert int32_to_ip(0) == "0.0.0.0"
assert int32_to_ip(2149583361) == "128.32.10.1"


def zeros(n):
    count_zeros = 0
    while n:
        n //= 5
        count_zeros += n

    return count_zeros


assert zeros(0) == 0
assert zeros(6) == 1
assert zeros(30) == 7
assert zeros(1000) == 249


def bananas(s) -> set:
    result = set()
    pattern = 'banana'
    for item in itertools.combinations(range(len(s)), len(s) - len(pattern)):
        combination = list(s)
        for pos in item:
            combination[pos] = '-'

        tmp = ''.join(combination)
        if tmp.replace('-', '') == pattern:
            result.add(tmp)

    return result


assert bananas("banann") == set()
assert bananas("banana") == {"banana"}
assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                                "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                                "-ban--ana", "b-anana--"}
assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}


def count_find_num(primesL, limit):
    result = []
    powers = []
    for prime in primesL:
        max_pwr = math.floor(math.log(limit, prime))
        powers.append(range(1, max_pwr + 1))

    for item in itertools.product(*powers):
        num = 1
        for i, el in enumerate(item):
            num *= pow(primesL[i], el)
        if num <= limit and num not in result:
            result.append(num)

    return [len(result), max(result)] if result else []


primesL = [2, 5, 7]
limit = 500
assert count_find_num(primesL, limit) == [5, 490]

primesL = [2, 3]
limit = 200
assert count_find_num(primesL, limit) == [13, 192]

primesL = [2, 5]
limit = 200
assert count_find_num(primesL, limit) == [8, 200]

primesL = [2, 3, 5]
limit = 500
assert count_find_num(primesL, limit) == [12, 480]

primesL = [2, 3, 5]
limit = 1000
assert count_find_num(primesL, limit) == [19, 960]

primesL = [2, 3, 47]
limit = 200
assert count_find_num(primesL, limit) == []

primesL = [29, 47, 89]
limit = 7541898
assert count_find_num(primesL, limit) == [3, 5701429]
