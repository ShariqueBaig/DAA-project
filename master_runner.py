"""
Master Runner - Complete DLP Analysis Workflow
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    try:
        import matplotlib
        import numpy
        import sympy
        print("✓ All dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nRun: pip install matplotlib numpy sympy")
        return False

def run_benchmark():
    print("\n" + "="*70)
    print("STAGE 1: Running Benchmark Suite")
    print("="*70)
    print("Testing 4 algorithms with hard 10-minute timeout")
    print("Expected duration: 20-60 minutes")
    print("-"*70)
    
    response = input("Start benchmark? (y/n): ").lower()
    if response != 'y':
        return False
    
    start = time.perf_counter()
    result = subprocess.run([sys.executable, "benchmark.py"], capture_output=False)
    elapsed = time.perf_counter() - start
    
    if result.returncode == 0:
        print(f"\n✓ Benchmark completed in {elapsed/60:.1f} minutes")
        return True
    else:
        print(f"\n✗ Benchmark failed")
        return False

def run_visualization():
    print("\n" + "="*70)
    print("STAGE 2: Generating Visualizations")
    print("="*70)
    
    if not os.path.exists("benchmark_results.csv"):
        print("✗ benchmark_results.csv not found")
        return False
    
    result = subprocess.run([sys.executable, "visualize.py"], capture_output=False)
    return result.returncode == 0

def main():
    print("\n" + "="*70)
    print("  DLP ALGORITHM ANALYSIS - MASTER RUNNER")
    print("="*70)
    print("\nAlgorithms: Brute Force, BSGS, Pollard's Rho, Pohlig-Hellman")
    print("Hard Timeout: 600 seconds (10 minutes)")
    print("\n" + "="*70)
    
    if not check_dependencies():
        return
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if run_benchmark():
        run_visualization()
        print("\n✓ Analysis complete!")
        print("  Graphs saved to ./graphs/")
    else:
        print("\nBenchmark failed. Run components individually:")
        print("  python benchmark.py")
        print("  python visualize.py")

if __name__ == "__main__":
    main()