from hypothesis import given, strategies as st
from heap.heap import Heap
import heapq
from ddmin import DDMin

def test_heap() -> None:
    heap = Heap()
    heap.push(3_567_111)    # heap: {3_567_111}
    heap.push(1_678_001)    # heap: {1_678_001, 3_567_111}
    heap.peek()             # returns 1_678_001 (root = smallest value)
    heap.push(2_345_678)    # heap: {1_678_001, 2_345_678, 3_567_111}
    heap.push(2_345_678)    # heap: {1_678_001, 2_345_678, 2_345_678, 3_567_111}
    heap.pop()              # removes the smallest value (1_678_001) --> heap: {2_345_678, 2_345_678, 3_567_111}
    heap.peek()             # returns 2_345_678 (new smallest value)
    heap.push(2_345_678)    # heap: {2_345_678, 2_345_678, 2_345_678, 3_567_111}
    heap.push(1_678_001)    # heap: {1_678_001, 2_345_678, 2_345_678, 2_345_678, 3_567_111}
    heap.pop()              # removes 1_678_001 (current smallest)
    heap.pop()              # removes 2_345_678 (current smallest)
    assert heap.peek() == 1_678_001

# initial check against heapq to see if bug is in heap.py
def test_heap_vs_heapq() -> None:
    """Compare python heapq vs program generated heap.
    Proves that the program's heap works correctly.
    CMD: uv run pytest test/heap/test_heap.py::test_heap_vs_heapq"""
    h, ref = Heap(), []

    def push(x): h.push(x); heapq.heappush(ref, x)
    def pop():   assert h.pop()  == heapq.heappop(ref)
    def peek():  assert h.peek() == ref[0]

    push(3_567_111); push(1_678_001); peek()
    push(2_345_678); push(2_345_678); pop(); peek()
    push(2_345_678); push(1_678_001); pop(); pop()

    assert h.peek() == ref[0]

# checking heap vs heapq to find minimal failing input
@given(st.lists(st.tuples(
    st.sampled_from(["push", "pop"]),
    st.integers(min_value=0, max_value=10),  # small range -> more duplicates
)))
def test_heap_matches_heapq(ops):
    """
    Compare python heapq vs program generated heap
    on random sequences of push/pop until divergence.
    """
    h, ref = Heap(), []
    for kind, arg in ops:
        if kind == "push":
            h.push(arg); heapq.heappush(ref, arg)
        elif kind == "pop" and ref:
            assert h.pop() == heapq.heappop(ref)

# shrinking the falsifying example with ddmin
def test_ddmin():
    """
    uv run pytest test/heap/test_heap.py::test_ddmin -s
    """
    false_ops = [("push", 0), ("push", 0), ("push", 0),
                 ("push", 1), ("push", 2),
                 ("pop", 0),  ("pop", 0),  ("pop", 0)]

    def passes(subset):
        h, ref = Heap(), []
        for kind, arg in subset:
            if kind == "push":
                h.push(arg); heapq.heappush(ref, arg)
            elif kind == "pop" and ref:
                if h.pop() != heapq.heappop(ref):
                    return False
        return True

    print(DDMin(false_ops, passes).execute())
