"""
Expanded Benchmarking Suite for DLP Algorithms
Adds more test cases, input variations, and detailed logging.
Usage: python expanded_benchmark.py
"""
import csv, time, os, random, math
from dlp_algorithms import brute_force, bsgs, pollards_rho, pohlig_hellman, prime_factors

# ─────────────────────────────────────────────────────────────────────────────
# Expanded Test Cases with More Diversity
# ─────────────────────────────────────────────────────────────────────────────
# (name, bit_length, generator, secret_x, prime, is_smooth, description)

BASE_TEST_CASES = [
    # ── Small primes (all 4 algorithms) ──
    ("Tiny Prime",     16, 3, 1543,       65537,       False, "Basic 16-bit test"),
    ("Small Prime",    20, 2, 45678,      1048583,     False, "20-bit non-smooth"),
    ("Medium Prime",   24, 5, 1234567,    16777259,    False, "24-bit standard"),
    ("Smooth Prime",   26, 7, 1234567,    106696591,   True,  "26-bit smooth p-1"),
    ("Hard Prime",     28, 3, 12345678,   268435459,   False, "28-bit non-smooth"),

    # ── Larger primes (selective algorithms) ──
    ("Large Prime",    32, 2, 123456789,  4294967311,  False, "32-bit large"),
    ("XL Prime",       40, 2, 987654321,  1099511627791, False, "40-bit extra large"),
]

# Additional generated cases for diversity
GENERATED_SMOOTH_CASES = []  # Will be populated dynamically
GENERATED_RANDOM_CASES = []  # Random primes with varying generators

BRUTE_FORCE_MAX_BITS = 28
POHLIG_MAX_BITS_NONSMOOTH = 28
BRUTE_FORCE_TIMEOUT = 60
CSV_FILE = "expanded_results.csv"

ALGORITHMS = [
    ("Brute Force",          brute_force),
    ("Baby-step Giant-step", bsgs),
    ("Pollard's Rho",        pollards_rho),
    ("Pohlig-Hellman",       pohlig_hellman),
]

def generate_random_prime(bits, max_attempts=1000):
    """Generate a random prime of approximately 'bits' bits."""
    from sympy import isprime
    for _ in range(max_attempts):
        candidate = random.getrandbits(bits)
        if candidate.bit_length() == bits and isprime(candidate):
            return candidate
    return None

def generate_smooth_prime(target_bits, max_seconds=30):
    """Generate a prime p where p-1 is B-smooth."""
    from sympy import isprime
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    start = time.perf_counter()
    for _ in range(500000):
        if time.perf_counter() - start > max_seconds:
            return None
        n = 2
        while n.bit_length() < target_bits - 2:
            n *= random.choice(small_primes)
        for mult in small_primes:
            candidate = n * mult
            if target_bits - 1 <= candidate.bit_length() <= target_bits + 1:
                p = candidate + 1
                if isprime(p):
                    return p
    return None

def find_generator(p):
    """Find a primitive root mod p."""
    N = p - 1
    factors = prime_factors(N)
    for g in range(2, min(1000, p)):
        if all(pow(g, N // q, p) != 1 for q in factors):
            return g
    return 2

def should_skip(algo_name, bits, is_smooth):
    """Decide whether to skip an algorithm."""
    if algo_name == "Brute Force" and bits > BRUTE_FORCE_MAX_BITS:
        return True, "Prime too large for brute force"
    if algo_name == "Pohlig-Hellman" and bits > POHLIG_MAX_BITS_NONSMOOTH and not is_smooth:
        return True, "Non-smooth prime too large for PH"
    return False, ""

def run_expanded_benchmark():
    print("=" * 80)
    print("  Expanded DLP Algorithm Benchmarking Suite")
    print("=" * 80)

    all_tests = list(BASE_TEST_CASES)

    # Generate additional smooth primes for diversity
    print("\n[*] Generating additional smooth primes for diversity...")
    for bits in [32, 36, 40, 44, 48]:
        sp = generate_smooth_prime(bits, max_seconds=20)
        if sp:
            g = find_generator(sp)
            x = random.randint(1, sp - 2)
            all_tests.append((f"Smooth ({bits}-bit)", bits, g, x, sp, True, f"Generated {bits}-bit smooth"))
            GENERATED_SMOOTH_CASES.append((bits, sp))
        else:
            print(f"    [!] Timeout generating {bits}-bit smooth prime")

    # Generate random primes for more variety
    print("\n[*] Generating random primes for input diversity...")
    for bits in [18, 22, 26, 30, 34]:
        rp = generate_random_prime(bits)
        if rp:
            g = find_generator(rp)
            x = random.randint(1, rp - 2)
            is_smooth = len(prime_factors(rp - 1)) <= 5  # Rough smoothness check
            all_tests.append((f"Random ({bits}-bit)", bits, g, x, rp, is_smooth, f"Random {bits}-bit {'smooth' if is_smooth else 'non-smooth'}"))
            GENERATED_RANDOM_CASES.append((bits, rp))

    results = []
    headers = ["bit_length", "prime", "test_name", "is_smooth", "description",
               "algorithm", "time_seconds", "result", "status", "memory_estimate"]

    for test_name, bits, g, x_true, p, is_smooth, desc in all_tests:
        h = pow(g, x_true, p)
        print(f"\n{'_'*80}")
        print(f"  Test: {test_name} | {bits}-bit | p = {p}")
        print(f"  Desc: {desc}")
        print(f"  Goal: {g}^x = {h} (mod {p}) | Expected x = {x_true}")

        for algo_name, func in ALGORITHMS:
            skip, reason = should_skip(algo_name, bits, is_smooth)
            if skip:
                print(f"  [SKIPPED] {algo_name:<25} | {reason}")
                results.append(dict(bit_length=bits, prime=p, test_name=test_name,
                    is_smooth=is_smooth, description=desc, algorithm=algo_name,
                    time_seconds=None, result=None, status="SKIPPED", memory_estimate=None))
                continue

            try:
                start = time.perf_counter()
                if algo_name == "Brute Force":
                    res = func(g, h, p, timeout=BRUTE_FORCE_TIMEOUT)
                else:
                    res = func(g, h, p)
                elapsed = time.perf_counter() - start

                # Estimate memory usage
                if algo_name == "Baby-step Giant-step":
                    mem_est = math.ceil(math.sqrt(p)) * 28  # Rough bytes for dict
                else:
                    mem_est = 1000  # Constant for others

                if res == "TIMEOUT":
                    status = "TIMEOUT"
                    print(f"  [TIMEOUT] {algo_name:<25} | >{BRUTE_FORCE_TIMEOUT}s | Mem: ~{mem_est} bytes")
                elif res is not None and pow(g, res, p) == h:
                    status = "PASSED"
                    print(f"  [PASSED ] {algo_name:<25} | {elapsed:.6f}s | Mem: ~{mem_est} bytes")
                else:
                    status = "FAILED"
                    print(f"  [FAILED ] {algo_name:<25} | {elapsed:.6f}s | Mem: ~{mem_est} bytes | got {res}")

                results.append(dict(bit_length=bits, prime=p, test_name=test_name,
                    is_smooth=is_smooth, description=desc, algorithm=algo_name,
                    time_seconds=elapsed, result=res, status=status, memory_estimate=mem_est))
            except Exception as e:
                print(f"  [ERROR  ] {algo_name:<25} | {e}")
                results.append(dict(bit_length=bits, prime=p, test_name=test_name,
                    is_smooth=is_smooth, description=desc, algorithm=algo_name,
                    time_seconds=None, result=None, status=f"ERROR: {e}", memory_estimate=None))

    # Write CSV
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(results)

    print(f"\n{'='*80}")
    print(f"  {len(results)} records written to {CSV_FILE}")
    print(f"  Generated {len(GENERATED_SMOOTH_CASES)} smooth and {len(GENERATED_RANDOM_CASES)} random test cases")

    print(f"\n  Done! Run 'python ../visualize.py' to generate graphs.")

if __name__ == "__main__":
    run_expanded_benchmark()