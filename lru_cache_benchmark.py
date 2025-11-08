import random
import time
from functools import lru_cache
from colorama import Fore, Style

# Generate a random array
N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

# Generate queries
Q = 50_000
queries = []
for _ in range(Q):
    if random.random() < 0.7:  # 70% of queries are Range
        L, R = sorted(random.sample(range(N), 2))
        queries.append(("Range", L, R))
    else:  # 30% of queries are Update
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))


# Functions without cache
def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


# LRU cache
CACHE_SIZE = 1000


@lru_cache(maxsize=CACHE_SIZE)
def range_sum_with_cache(L, R):
    return sum(array[L : R + 1])


def update_with_cache(array, index, value):
    # Any update invalidates all cached range sums
    array[index] = value
    range_sum_with_cache.cache_clear()


# Measure execution time without cache
print(Fore.YELLOW + "Running benchmark without cache..." + Style.RESET_ALL)
start = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
end = time.time()
time_no_cache = end - start
print(
    Fore.RED
    + f"Execution time without caching: {time_no_cache:.2f} seconds"
    + Style.RESET_ALL
)

# Measure execution time with LRU cache
print(Fore.YELLOW + "Running benchmark with LRU cache..." + Style.RESET_ALL)
start = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
end = time.time()
time_with_cache = end - start
print(
    Fore.GREEN
    + f"Execution time with LRU cache: {time_with_cache:.2f} seconds"
    + Style.RESET_ALL
)

# Compare results
if time_with_cache < time_no_cache:
    speed_up = time_no_cache / time_with_cache
    print(Fore.CYAN + f"Cache is {speed_up:.2f}× faster!" + Style.RESET_ALL)
else:
    print(Fore.RED + "Cache did not improve speed!" + Style.RESET_ALL)
