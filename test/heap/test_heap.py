from heap.heap import Heap


def test_heap() -> None:
    heap = Heap()
    heap.push(3_567_111)
    heap.push(1_678_001)
    heap.peek()
    heap.push(2_345_678)
    heap.push(2_345_678)
    heap.pop()
    heap.peek()
    heap.push(2_345_678)
    heap.push(1_678_001)
    heap.pop()
    heap.pop()
    assert heap.peek() == 1_678_001
