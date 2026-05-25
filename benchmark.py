"""
DLP Benchmarking Suite - 4 Algorithms, Hard 10-min Timeout
"""

import csv
import os
import time
import sys
import math
import random
from datetime import datetime

# Import algorithms
from dlp_algorithms import (
    brute_force, bsgs, pollards_rho, pohlig_hellman,
    generate_smooth_prime, generate_hard_prime, generate_prime,
    find_primitive_root, prime_factors
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Hard timeout: 10 minutes = 600 seconds for ALL algorithms
HARD_TIMEOUT = 600

# Bit lengths to test - extensive but reasonable
BIT_LENGTHS = [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]

# Maximum bits per algorithm
MAX_BITS_PER_ALGO = {
    "Brute Force": 32,
    "BSGS": 50,
    "Pollard's Rho": 54,
    "Pohlig-Hellman": 54
}

# Output file
OUTPUT_CSV = "benchmark_results.csv"

# Algorithms
ALGORITHMS = {
    "Brute Force": {"func": brute_force, "timeout": HARD_TIMEOUT},
    "BSGS": {"func": bsgs, "timeout": HARD_TIMEOUT},
    "Pollard's Rho": {"func": pollards_rho, "timeout": HARD_TIMEOUT},
    "Pohlig-Hellman": {"func": pohlig_hellman, "timeout": HARD_TIMEOUT}
}

# Datasets
DATASETS = {
    "weak": {
        "generator": generate_smooth_prime,
        "description": "Weak primes - p-1 has ONLY small factors (all <= 53)",
        "color": "#e74c3c"
    },
    "random": {
        "generator": generate_prime,
        "description": "Random primes - standard cryptographic primes",
        "color": "#3498db"
    },
    "hard": {
        "generator": generate_hard_prime,
        "description": "Hard primes - p = 2q+1 (safe primes), p-1 has ONE large factor",
        "color": "#2ecc71"
    }
}

# ============================================================================
# BENCHMARK CLASS
# ============================================================================

class Benchmark:
    def __init__(self):
        self.results = []
        self.test_id = 0
        self.start_time = time.perf_counter()
        
    def generate_test_case(self, bits, dataset_type):
        """Generate a test case with exponent in the LATER half (70-95% range)"""
        generator_func = DATASETS[dataset_type]["generator"]
        
        # Generate prime
        p = generator_func(bits)
        if p is None:
            return None
        
        # Find primitive root generator
        g = find_primitive_root(p)
        
        # Generate exponent in the LATER half for better analysis
        # Use 70-95% of the range to make brute force search harder
        max_x = p - 2
        lower_bound = int(max_x * 0.7)  # Start at 70%
        upper_bound = int(max_x * 0.95)  # End at 95%
        
        # Ensure we have valid range
        if lower_bound >= upper_bound:
            lower_bound = max_x // 2
        
        x = random.randint(lower_bound, upper_bound)
        
        # Compute h
        h = pow(g, x, p)
        
        return {
            "bit_length": bits,
            "prime": p,
            "generator": g,
            "exponent": x,
            "target": h,
            "dataset": dataset_type,
            "p_minus_1_factors": prime_factors(p-1),
            "exponent_position": f"{x}/{max_x} ({100*x/max_x:.1f}%)"
        }
    
    def run_algorithm(self, algo_name, algo_config, test_case):
        """Run a single algorithm on a test case with hard timeout"""
        bits = test_case["bit_length"]
        p = test_case["prime"]
        g = test_case["generator"]
        h = test_case["target"]
        expected = test_case["exponent"]
        
        # Skip if beyond reasonable bit length for this algorithm
        if bits > MAX_BITS_PER_ALGO.get(algo_name, 60):
            return {
                "status": "SKIPPED",
                "time": None,
                "result": None,
                "timeout_occurred": False
            }
        
        # Run algorithm with timeout
        timeout = algo_config["timeout"]
        func = algo_config["func"]
        
        try:
            start = time.perf_counter()
            result, status = func(g, h, p, timeout=timeout)
            elapsed = time.perf_counter() - start
            
            # Check if timeout occurred
            timeout_occurred = (status == "TIMEOUT" or elapsed >= timeout - 1)
            
            if timeout_occurred:
                return {
                    "status": "TIMEOUT",
                    "time": timeout,
                    "result": None,
                    "timeout_occurred": True
                }
            
            # Verify result
            if result is not None and pow(g, result, p) == h:
                return {
                    "status": "PASSED",
                    "time": elapsed,
                    "result": result,
                    "timeout_occurred": False
                }
            else:
                return {
                    "status": "FAILED",
                    "time": elapsed,
                    "result": result,
                    "timeout_occurred": False
                }
                
        except Exception as e:
            return {
                "status": f"ERROR: {str(e)[:50]}",
                "time": None,
                "result": None,
                "timeout_occurred": False
            }
    
    def estimate_memory(self, algo_name, bits):
        """Estimate memory usage for an algorithm"""
        if algo_name == "BSGS":
            p_approx = 1 << bits
            entries = int(math.isqrt(p_approx))
            return entries * 72
        elif algo_name in ["Brute Force", "Pollard's Rho"]:
            return 1024
        elif algo_name == "Pohlig-Hellman":
            return 2048
        else:
            return 8192
    
    def run_all(self):
        """Run complete benchmark"""
        print("\n" + "="*80)
        print("  DLP ALGORITHM BENCHMARKING SUITE")
        print("="*80)
        print(f"  HARD TIMEOUT: {HARD_TIMEOUT} seconds ({HARD_TIMEOUT/60} minutes)")
        print(f"  Bit lengths: {BIT_LENGTHS}")
        print(f"  Datasets: {', '.join(DATASETS.keys())}")
        print(f"  Exponents: Generated in LATER half (70-95% of range)")
        print("="*80)
        
        total_tests = len(BIT_LENGTHS) * len(DATASETS) * len(ALGORITHMS)
        completed = 0
        
        for bits in BIT_LENGTHS:
            for dataset_name, dataset_config in DATASETS.items():
                print(f"\n{'='*80}")
                print(f"  Testing: {bits}-bit | Dataset: {dataset_name.upper()}")
                print(f"  {dataset_config['description']}")
                print(f"{'='*80}")
                
                # Generate test case
                test_case = self.generate_test_case(bits, dataset_name)
                if test_case is None:
                    print(f"  ✗ Failed to generate test case for {bits}-bit {dataset_name}")
                    continue
                
                print(f"  Prime: {test_case['prime']}")
                print(f"  Generator: {test_case['generator']}")
                print(f"  Expected x: {test_case['exponent']} ({test_case['exponent_position']})")
                factors_str = str(dict(list(test_case['p_minus_1_factors'].items())[:3]))
                print(f"  p-1 factors: {factors_str}...")
                print(f"\n  {'Algorithm':<20} {'Status':<12} {'Time (s)':<12} {'Result':<20}")
                print(f"  {'-'*70}")
                
                for algo_name, algo_config in ALGORITHMS.items():
                    # Run algorithm
                    result_data = self.run_algorithm(algo_name, algo_config, test_case)
                    
                    # Estimate memory
                    memory_est = self.estimate_memory(algo_name, bits)
                    
                    # Store result
                    self.results.append({
                        "test_id": self.test_id,
                        "bit_length": bits,
                        "dataset": dataset_name,
                        "prime": test_case["prime"],
                        "generator": test_case["generator"],
                        "expected_x": test_case["exponent"],
                        "exponent_position": test_case["exponent_position"],
                        "target_h": test_case["target"],
                        "algorithm": algo_name,
                        "status": result_data["status"],
                        "time_seconds": result_data["time"] if result_data["time"] is not None else -1,
                        "result_x": result_data["result"] if result_data["result"] else "",
                        "timeout_occurred": result_data["timeout_occurred"],
                        "memory_estimate_bytes": memory_est
                    })
                    
                    # Print result
                    time_str = f"{result_data['time']:.2f}" if result_data['time'] and result_data['time'] > 0 else "TIMEOUT"
                    status_symbol = "✓" if result_data["status"] == "PASSED" else "⏰" if result_data["timeout_occurred"] else "✗"
                    
                    print(f"  {algo_name:<20} {status_symbol} {result_data['status']:<10} {time_str:<12} {str(result_data['result'])[:20]}")
                    
                    completed += 1
                    progress = completed / total_tests * 100
                    sys.stdout.write(f"\r  Progress: {progress:.1f}% ({completed}/{total_tests})")
                    sys.stdout.flush()
                
                self.test_id += 1
                print()
        
        print(f"\n\n{'='*80}")
        print(f"  BENCHMARK COMPLETE!")
        print(f"  Total tests: {len(self.results)}")
        print(f"  Time taken: {(time.perf_counter() - self.start_time)/60:.1f} minutes")
        print(f"{'='*80}")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save results to CSV"""
        with open(OUTPUT_CSV, 'w', newline='') as f:
            fieldnames = [
                "test_id", "bit_length", "dataset", "prime", "generator",
                "expected_x", "exponent_position", "target_h", "algorithm", 
                "status", "time_seconds", "result_x", "timeout_occurred", 
                "memory_estimate_bytes"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"\n  Results saved to: {OUTPUT_CSV}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    benchmark = Benchmark()
    benchmark.run_all()