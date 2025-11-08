import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from colorama import Fore, Style, init
from typing import List, Tuple, Optional

init(autoreset=True)


# LRU Cache implementation for computing Fibonacci numbers
@lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    """Fibonacci with unbounded LRU cache (top–down memoization)."""
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Splay Tree implementation used as a memo store for Fibonacci numbers
class SplayTreeNode:
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        self.left: Optional["SplayTreeNode"] = None
        self.right: Optional["SplayTreeNode"] = None


class SplayTree:
    def __init__(self):
        self.root: Optional[SplayTreeNode] = None

    def splay(self, node: Optional[SplayTreeNode], key: int) -> Optional[SplayTreeNode]:
        """Move the node with `key` (or the last accessed node) to root."""
        if not node:
            return node

        if key == node.key:
            return node

        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self.splay(node.left.left, key)
                node = self.rotate_right(node)
            elif key > node.left.key:
                node.left.right = self.splay(node.left.right, key)
                if node.left.right:
                    node.left = self.rotate_left(node.left)
            return node if not node.left else self.rotate_right(node)
        else:
            if not node.right:
                return node
            if key < node.right.key:
                node.right.left = self.splay(node.right.left, key)
                if node.right.left:
                    node.right = self.rotate_right(node.right)
            return node if not node.right else self.rotate_left(node)

    def rotate_left(self, node: SplayTreeNode) -> SplayTreeNode:
        if not node or not node.right:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def rotate_right(self, node: SplayTreeNode) -> SplayTreeNode:
        if not node or not node.left:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def insert(self, key: int, value: int) -> None:
        """Insert or update a (key, value) pair, splaying around `key`."""
        self.root = self._insert(self.root, key, value)

    def _insert(self, node: Optional[SplayTreeNode], key: int, value: int) -> SplayTreeNode:
        if not node:
            return SplayTreeNode(key, value)
        node = self.splay(node, key)
        if key == node.key:
            node.value = value
            return node
        elif key < node.key:
            new_node = SplayTreeNode(key, value)
            new_node.left = node.left
            node.left = None
            node = self.rotate_right(node)
            new_node.right = node
            return new_node
        else:
            new_node = SplayTreeNode(key, value)
            new_node.right = node.right
            node.right = None
            node = self.rotate_left(node)
            new_node.left = node
            return new_node

    def find(self, key: int) -> Optional[int]:
        """Return the value for `key` if present; otherwise None (and splay last access)."""
        self.root = self.splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None


def fibonacci_splay(n: int, tree: SplayTree) -> int:
    """Fibonacci with a Splay Tree memo store."""
    cached = tree.find(n)
    if cached is not None:
        return cached
    if n <= 1:
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# Measure execution time for both LRU Cache and Splay Tree approaches
def measure_time() -> Tuple[List[int], List[float], List[float]]:
    ns = list(range(0, 1000, 50))
    lru_times: List[float] = []
    splay_times: List[float] = []

    tree = SplayTree()

    for n in ns:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(lru_time)

        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(splay_time)

    return ns, lru_times, splay_times


# Compare and plot execution times
def plot_results() -> None:
    ns, lru_times, splay_times = measure_time()

    # Text table with colored output
    print(
        f"{Fore.CYAN}{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}{Style.RESET_ALL}"
    )
    print(Fore.GREEN + "-" * 50 + Style.RESET_ALL)
    for n, lru_time, splay_time in zip(ns, lru_times, splay_times):
        print(
            f"{Fore.YELLOW}{n:<10}{Fore.RED}{lru_time:<25}{Fore.MAGENTA}{splay_time}{Style.RESET_ALL}"
        )

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(ns, lru_times, label="LRU Cache")
    plt.plot(ns, splay_times, label="Splay Tree")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Performance Comparison: LRU Cache vs. Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_results()
