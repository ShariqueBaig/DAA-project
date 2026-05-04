"""
Stress Testing Suite
Tests algorithms at memory and time limits to validate theoretical bounds.
Usage: python stress_test.py
"""
import time
import psutil
import os
from dlp_algorithms import brute_force, bsgs, pollards_rho, pohlig_hellman

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def stress_test_bsgs():
    """Stress test BSGS to find memory limits."""
    print("Stress Testing Baby-step Giant-step Memory Limits")
    print("=" * 60)

    # Start with 32-bit and increase
    bits = 32
    while bits <= 48:
        try:
            p = (1 << bits) - 1  # Mersenne prime approximation
            g = 2
            x = 12345 % (p - 1)
            h = pow(g, x, p)

            print(f"\nTesting {bits}-bit prime (p ≈ {p})")
            mem_before = get_memory_usage()
            start = time.perf_counter()

            result = bsgs(g, h, p)

            elapsed = time.perf_counter() - start
            mem_after = get_memory_usage()
            mem_used = mem_after - mem_before

            print(f"Time: {elapsed:.6f}s")
            print(f"Memory used: {mem_used:.2f} MB")
            print(f"Result: {result}")

            if mem_used > 1000:  # 1GB threshold
                print("WARNING: High memory usage detected")
                break

            bits += 4
        except MemoryError:
            print(f"MemoryError at {bits} bits")
            break
        except Exception as e:
            print(f"Error at {bits} bits: {e}")
            bits += 4

def stress_test_pollards_rho():
    """Stress test Pollard's Rho for large inputs."""
    print("\nStress Testing Pollard's Rho Scalability")
    print("=" * 60)

    bits = 40
    while bits <= 60:
        try:
            p = (1 << bits) + 1  # Approximate prime
            g = 2
            x = 98765 % (p - 1)
            h = pow(g, x, p)

            print(f"\nTesting {bits}-bit prime")
            mem_before = get_memory_usage()
            start = time.perf_counter()

            result = pollards_rho(g, h, p)

            elapsed = time.perf_counter() - start
            mem_after = get_memory_usage()
            mem_used = mem_after - mem_before

            print(f"Time: {elapsed:.6f}s")
            print(f"Memory used: {mem_used:.2f} MB")
            print(f"Result: {result}")

            bits += 4
        except Exception as e:
            print(f"Error at {bits} bits: {e}")
            break

def stress_test_brute_force_timeout():
    """Find timeout threshold for brute force."""
    print("\nStress Testing Brute Force Timeout Limits")
    print("=" * 60)

    bits = 28
    while bits <= 35:
        try:
            p = (1 << bits) - 1
            g = 2
            x = 123 % (p - 1)
            h = pow(g, x, p)

            print(f"\nTesting {bits}-bit prime (timeout 60s)")
            start = time.perf_counter()
            result = brute_force(g, h, p, timeout=60)
            elapsed = time.perf_counter() - start

            if result == "TIMEOUT":
                print(f"Timeout at {bits} bits after {elapsed:.2f}s")
                break
            else:
                print(f"Completed in {elapsed:.6f}s")
                bits += 1
        except Exception as e:
            print(f"Error at {bits} bits: {e}")
            break

def main():
    print("DLP Algorithm Stress Testing Suite")
    print("Testing theoretical limits and practical boundaries")
    print("=" * 80)

    try:
        stress_test_bsgs()
        stress_test_pollards_rho()
        stress_test_brute_force_timeout()
    except KeyboardInterrupt:
        print("\nStress testing interrupted by user")

    print("\nStress testing complete.")

if __name__ == "__main__":
    main()