"""
Master Runner - Orchestrates complete DLP analysis workflow
Runs all stages in recommended order with error handling.
Usage: python master_runner.py
"""
import os
import sys
import time
import subprocess

def run_stage(script_name, description, required=True):
    """Run a Python script and handle errors."""
    print(f"\n{'='*70}")
    print(f"Stage: {description}")
    print(f"Running: {script_name}")
    print(f"{'='*70}")
    
    try:
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            timeout=3600
        )
        elapsed = time.perf_counter() - start
        
        if result.returncode == 0:
            print(f"\n[✓] {description} completed in {elapsed:.1f}s")
            return True
        else:
            if required:
                print(f"\n[✗] {description} failed with code {result.returncode}")
                return False
            else:
                print(f"\n[!] {description} failed (optional, continuing)")
                return False
    except subprocess.TimeoutExpired:
        print(f"\n[✗] {description} timed out after 3600s")
        return False
    except Exception as e:
        if required:
            print(f"\n[✗] Error running {description}: {e}")
            return False
        else:
            print(f"\n[!] Error running {description}: {e} (optional, continuing)")
            return False

def main():
    print("\n" + "="*70)
    print("DLP Algorithm Analysis - Master Runner")
    print("="*70)
    print("This script orchestrates the complete analysis workflow.")
    print("Recommended execution order:")
    print("  1. Expanded Benchmarking (required)")
    print("  2. Visualization Generation (required)")
    print("  3. Optional advanced testing")
    print("="*70)

    # Check Python version
    if sys.version_info < (3, 8):
        print("[✗] Python 3.8+ required")
        return False

    # Check dependencies
    try:
        import matplotlib
        import sympy
    except ImportError as e:
        print(f"\n[!] Missing dependency: {e}")
        print("    Run: pip install -r requirements.txt")
        return False

    # Stage 1: Expanded Benchmarking (Required)
    print("\n[*] Stage 1: Core Benchmarking")
    if not os.path.exists("dlp_algorithms.py"):
        print("[✗] dlp_algorithms.py not found in current directory")
        return False
    
    if not run_stage("expanded_benchmark.py", "Expanded Benchmarking", required=True):
        print("\n[✗] Benchmarking failed - cannot proceed")
        return False

    # Stage 2: Visualization (Required)
    print("\n[*] Stage 2: Visualization Generation")
    if not run_stage("visualize_analysis.py", "Visualization Generation", required=True):
        print("\n[✗] Visualization failed")
        return False

    # Stage 3a: Parallel Processing (Optional)
    print("\n[*] Stage 3a: Parallel Processing Validation (Optional)")
    run_stage("parallel_brute_force.py", "Parallel Brute Force", required=False)

    # Stage 3b: Enhanced PH (Optional)
    print("\n[*] Stage 3b: Enhanced Pohlig-Hellman (Optional)")
    run_stage("enhanced_pohlig_hellman.py", "Enhanced Pohlig-Hellman", required=False)

    # Stage 3c: Stress Testing (Optional, with warning)
    print("\n[*] Stage 3c: Stress Testing (Optional)")
    response = input("Run stress testing? This may take 5-60 minutes and use significant RAM. (y/n): ")
    if response.lower() == 'y':
        run_stage("stress_test.py", "Stress Testing", required=False)

    # Summary
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)
    print("\nGenerated files:")
    print("  - expanded_results.csv (benchmark data)")
    print("  - graphs/runtime_vs_bits.png")
    print("  - graphs/smooth_vs_nonsmooth.png")
    print("  - graphs/memory_analysis.png")
    print("  - graphs/algorithm_comparison.png")
    print("\nNext steps:")
    print("  1. Review expanded_results.csv for raw data")
    print("  2. View PNG graphs for visual analysis")
    print("  3. Consult RUN_ORDER.md for detailed documentation")
    print("="*70)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
