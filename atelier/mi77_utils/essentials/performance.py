import time
import tracemalloc
from contextlib import contextmanager


@contextmanager
def perf_profile(name=None):

    tracemalloc.start()

    memory_before, _ = tracemalloc.get_traced_memory()

    wall_start = time.perf_counter()
    cpu_start = time.process_time()

    try:
        yield
    finally:
        wall_time = time.perf_counter() - wall_start
        cpu_time = time.process_time() - cpu_start

        memory_after, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        mb = 1024 ** 2

        if name:
            print(f"Code Block: {name}")
        print(f"Execution Time: {wall_time:.6f} s")
        print(f"CPU Time: {cpu_time:.6f} s")
        print(f"Memory Usage Before: {memory_before / mb:.2f} MB")
        print(f"Memory Usage After: {memory_after / mb:.2f} MB")
        print(f"Peak Traced Memory: {peak / mb:.2f} MB")