"""
Selective Benchmark - Brute Force and Pohlig-Hellman only
"""
import csv
import os
import sys
import time
import math
import random
from datetime import datetime
from sympy import isprime, randprime

# Import algorithms
from dlp_algorithms import brute_force, pohlig_hellman, find_primitive_root, prime_factors

HARD_TIMEOUT = 600
BIT_LENGTHS = [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]
DATASETS = ["weak", "random", "hard"]
ALGORITHMS_TO_RUN = ["Brute Force", "Pohlig-Hellman"]

def generate_prime(bits):
    lower = 1 << (bits - 1)
    upper = (1 << bits) - 1
    try:
        return randprime(lower, upper)
    except:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        while not isprime(candidate):
            candidate += 2
            if candidate > upper:
                candidate = lower | 1
        return candidate

def generate_smooth_prime(bits, max_seconds=60):
    from sympy import isprime
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    start_time = time.perf_counter()
    while (time.perf_counter() - start_time) < max_seconds:
        n = 1
        while n.bit_length() < bits - 2:
            n *= random.choice(small_primes)
        p = n + 1
        if p.bit_length() == bits and isprime(p):
            factors = prime_factors(p-1)
            if all(f <= 53 for f in factors):
                return p
    return None

def generate_hard_prime(bits, max_attempts=100):
    from sympy import isprime
    for _ in range(max_attempts):
        q = generate_prime(bits - 1)
        if q is None:
            continue
        p = 2 * q + 1
        if isprime(p):
            return p
    return generate_prime(bits)

DATASET_GENERATORS = {
    "weak": generate_smooth_prime,
    "random": generate_prime,
    "hard": generate_hard_prime
}

def generate_test_case(bits, dataset_type):
    generator_func = DATASET_GENERATORS[dataset_type]
    p = generator_func(bits)
    if p is None:
        return None
    
    g = find_primitive_root(p)
    max_x = p - 2
    lower_bound = int(max_x * 0.7)
    upper_bound = int(max_x * 0.95)
    if lower_bound >= upper_bound:
        lower_bound = max_x // 2
    x = random.randint(lower_bound, upper_bound)
    h = pow(g, x, p)
    
    return {
        "bit_length": bits,
        "prime": p,
        "generator": g,
        "exponent": x,
        "target": h,
        "dataset": dataset_type,
        "exponent_position": f"{x}/{max_x} ({100*x/max_x:.1f}%)"
    }

def run_algorithm(algo_name, g, h, p, timeout=600):
    start = time.perf_counter()
    if algo_name == "Brute Force":
        result, status = brute_force(g, h, p, timeout=timeout)
    else:
        result, status = pohlig_hellman(g, h, p, timeout=timeout)
    elapsed = time.perf_counter() - start
    
    timeout_occurred = (status == "TIMEOUT" or elapsed >= timeout - 1)
    
    if timeout_occurred:
        return {"status": "TIMEOUT", "time": timeout, "result": None, "timeout_occurred": True}
    elif result is not None and pow(g, result, p) == h:
        return {"status": "PASSED", "time": elapsed, "result": result, "timeout_occurred": False}
    else:
        return {"status": "FAILED", "time": elapsed, "result": result, "timeout_occurred": False}

def estimate_memory(algo_name, bits):
    if algo_name == "Brute Force":
        return 1024
    elif algo_name == "Pohlig-Hellman":
        return 4096
    else:
        return 8192

def main():
    results = []
    test_id = 0
    
    print("\nSelective Benchmarking: Brute Force & Pohlig-Hellman")
    print("="*60)
    
    for bits in BIT_LENGTHS:
        for dataset in DATASETS:
            print(f"\nTesting {bits}-bit {dataset} prime...")
            
            test_case = generate_test_case(bits, dataset)
            if test_case is None:
                print(f"  Failed to generate test case")
                continue
            
            for algo in ALGORITHMS_TO_RUN:
                result_data = run_algorithm(algo, test_case["generator"], 
                                           test_case["target"], test_case["prime"])
                memory_est = estimate_memory(algo, bits)
                
                results.append({
                    "test_id": test_id,
                    "bit_length": bits,
                    "dataset": dataset,
                    "prime": test_case["prime"],
                    "generator": test_case["generator"],
                    "expected_x": test_case["exponent"],
                    "exponent_position": test_case["exponent_position"],
                    "target_h": test_case["target"],
                    "algorithm": algo,
                    "status": result_data["status"],
                    "time_seconds": result_data["time"] if result_data["time"] else -1,
                    "result_x": result_data["result"] if result_data["result"] else "",
                    "timeout_occurred": result_data["timeout_occurred"],
                    "memory_estimate_bytes": memory_est
                })
                
                status_symbol = "OK" if result_data["status"] == "PASSED" else "TO" if result_data["timeout_occurred"] else "ER"
                time_str = f"{result_data['time']:.2f}" if result_data['time'] else "TIMEOUT"
                print(f"  {status_symbol} {algo}: {time_str}s")
            
            test_id += 1
    
    # Save new results
    new_results_file = "new_bf_ph_results.csv"
    with open(new_results_file, 'w', newline='') as f:
        fieldnames = ["test_id", "bit_length", "dataset", "prime", "generator",
                     "expected_x", "exponent_position", "target_h", "algorithm",
                     "status", "time_seconds", "result_x", "timeout_occurred",
                     "memory_estimate_bytes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n\nNew results saved to: {new_results_file}")
    return new_results_file

if __name__ == "__main__":
    main()
