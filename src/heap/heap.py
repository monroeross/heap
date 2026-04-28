from .queue import PriorityQueue


class Heap(PriorityQueue):
    def __init__(self):
        self._data: list[int] = []

    def push(self, x: int) -> None:
        """Insert element"""
        self._data.append(x)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        """Remove and return smallest element"""
        if not self._data:
            raise IndexError("pop from empty priority queue")

        self._swap(0, len(self._data) - 1)
        x = self._data.pop()
        if self._data:
            self._sift_down(0)
        return x

    def peek(self):
        """Return smallest element without removing"""
        if not self._data:
            raise IndexError("peek from empty priority queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    # --- Internal helpers ---

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _sift_up(self, i: int):
        """Restore heap property going upward"""
        while i > 0:
            p = self._parent(i)
            if self._data[i] < self._data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i: int):
        """Restore heap property going downward"""
        n = len(self._data)
        while True:
            l = self._left(i)
            r = self._right(i)
            smallest = i

            if l < n and self._data[l] < self._data[smallest]:
                smallest = l
            elif r < n and self._data[r] < self._data[smallest]:
                smallest = r

            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest
