"""
Parallel Brute Force Implementation
Uses multiprocessing to parallelize brute force search across CPU cores.
Usage: python parallel_brute_force.py
"""
import multiprocessing as mp
import time
import math
from dlp_algorithms import brute_force  # For reference, but we'll implement parallel version

def brute_force_worker(g, h, p, start, end):
    """Worker function for parallel brute force."""
    for x in range(start, min(end, p)):
        if pow(g, x, p) == h:
            return x
    return None

def parallel_brute_force(g, h, p, num_processes=None, timeout=300):
    """Parallel brute force using multiprocessing."""
    if num_processes is None:
        num_processes = mp.cpu_count()

    start_time = time.perf_counter()
    chunk_size = math.ceil(p / num_processes)

    # Create process pool
    with mp.Pool(processes=num_processes) as pool:
        # Submit tasks
        futures = []
        for i in range(num_processes):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            future = pool.apply_async(brute_force_worker, (g, h, p, start, end))
            futures.append(future)

        # Wait for results with timeout
        for future in futures:
            try:
                result = future.get(timeout=timeout)
                if result is not None:
                    elapsed = time.perf_counter() - start_time
                    return result, elapsed
            except mp.TimeoutError:
                continue

        elapsed = time.perf_counter() - start_time
        return None, elapsed  # Timeout or not found

def test_parallel_brute_force():
    """Test the parallel brute force on sample inputs."""
    test_cases = [
        (3, 56755, 65537, 1543),      # 16-bit
        (2, 349042, 1048583, 45678),  # 20-bit
        (5, 2092104, 16777259, 1234567), # 24-bit
    ]

    print("Testing Parallel Brute Force")
    print("=" * 50)

    for g, h, p, expected in test_cases:
        print(f"\nTesting: {g}^x = {h} (mod {p})")
        print(f"Expected: x = {expected}")

        # Sequential for comparison
        start = time.perf_counter()
        seq_result = brute_force(g, h, p, timeout=60)
        seq_time = time.perf_counter() - start
        print(f"Sequential: {seq_time:.6f}s, Result: {seq_result}")

        # Parallel
        par_result, par_time = parallel_brute_force(g, h, p, timeout=60)
        print(f"Parallel:   {par_time:.6f}s, Result: {par_result}")

        # Verify
        if par_result == expected:
            speedup = seq_time / par_time if par_time > 0 else float('inf')
            print(f"Speedup: {speedup:.2f}x")
        else:
            print("ERROR: Parallel result incorrect")

if __name__ == "__main__":
    test_parallel_brute_force()