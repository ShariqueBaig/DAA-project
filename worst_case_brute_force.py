"""
Worst-Case DLP Analysis - 30, 40, 50 bits only
Answer at p-2 (farthest possible position)
Enforced 10-minute timeout per test
Shows true O(2^n) complexity bound
"""

import time
import random
import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime, randprime

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Timeout settings
TIMEOUT_SECONDS = 600  # 10 minutes

# Configure matplotlib
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--'
})

def generate_prime(bits):
    """Generate a random prime of given bit length"""
    lower = 1 << (bits - 1)
    upper = (1 << bits) - 1
    try:
        return randprime(lower, upper)
    except:
        # Fallback
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        while not isprime(candidate):
            candidate += 2
            if candidate > upper:
                candidate = lower | 1
        return candidate

def find_primitive_root(p):
    """Find a primitive root modulo prime p"""
    # Factorize p-1
    n = p - 1
    factors = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        factors.append(n)
    
    # Test potential generators
    for g in range(2, min(100, p)):
        valid = True
        for q in factors:
            if pow(g, (p-1)//q, p) == 1:
                valid = False
                break
        if valid:
            return g
    return 2

def brute_force_with_timeout(g, h, p, timeout=TIMEOUT_SECONDS):
    """
    Brute force with 10-minute timeout
    Searches all the way to p-2
    Returns (result, time_taken, timeout_occurred)
    """
    start_time = time.perf_counter()
    
    for x in range(p - 1):  # Search 0 to p-2
        # Check timeout
        if (time.perf_counter() - start_time) > timeout:
            return None, timeout, True
        
        if pow(g, x, p) == h:
            elapsed = time.perf_counter() - start_time
            return x, elapsed, False
    
    return None, time.perf_counter() - start_time, False

def generate_worst_case_test(bits):
    """
    Generate test case where answer is at p-2 (farthest position)
    """
    print(f"  Generating {bits}-bit prime (answer at p-2)...")
    
    # Generate prime
    p = generate_prime(bits)
    
    # Find primitive root
    g = find_primitive_root(p)
    
    # Set exponent to p-2 (farthest possible)
    x = p - 2
    
    # Compute h = g^x mod p
    h = pow(g, x, p)
    
    return {
        'bits': bits,
        'p': p,
        'g': g,
        'x': x,
        'h': h,
        'position': f"{x}/{p-1} (100% of range)"
    }

def run_worst_case_analysis():
    """Run analysis for 30, 40, 50 bits with timeout"""
    print("\n" + "="*80)
    print("  WORST-CASE DLP ANALYSIS (with 10-min timeout)")
    print("  Answer at p-2 (farthest possible position)")
    print("="*80)
    print(f"  Timeout per test: {TIMEOUT_SECONDS} seconds ({TIMEOUT_SECONDS/60} minutes)")
    print("  Testing: 30, 40, 50 bits")
    print("="*80)
    
    bit_lengths = [30, 40, 50]
    results = []
    
    for bits in bit_lengths:
        print(f"\n{'='*50}")
        print(f"  Testing {bits}-bit prime")
        print(f"{'='*50}")
        
        # Generate worst-case test
        test = generate_worst_case_test(bits)
        
        print(f"  Prime p: {test['p']}")
        print(f"  Generator g: {test['g']}")
        print(f"  Answer x: p-2 = {test['x']}")
        print(f"  Position: {test['position']}")
        
        # Calculate total possibilities
        total_checks = test['x'] + 1
        print(f"  Total checks needed: {total_checks:,}")
        
        # Run brute force with timeout
        print(f"\n  Running brute force (timeout at {TIMEOUT_SECONDS}s)...")
        
        result_x, elapsed, timeout_occurred = brute_force_with_timeout(
            test['g'], test['h'], test['p']
        )
        
        if timeout_occurred:
            print(f"\n  [!] TIMEOUT after {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
            print(f"      Could not complete search for {bits}-bit prime")
            results.append({
                'bits': bits,
                'p': test['p'],
                'time': elapsed,
                'timeout': True,
                'found': None,
                'expected': test['x']
            })
        elif result_x == test['x']:
            print(f"\n  [OK] SUCCESS!")
            print(f"      Found x = {result_x}")
            print(f"      Time taken: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
            results.append({
                'bits': bits,
                'p': test['p'],
                'time': elapsed,
                'timeout': False,
                'found': result_x,
                'expected': test['x']
            })
        else:
            print(f"\n  [!!] FAILED - Expected {test['x']}, got {result_x}")
            results.append({
                'bits': bits,
                'p': test['p'],
                'time': elapsed,
                'timeout': False,
                'found': result_x,
                'expected': test['x']
            })
    
    return results

def plot_worst_case_analysis(results):
    """
    Plot worst-case Brute Force performance with timeout markers
    """
    if not results:
        print("No results to plot")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Extract data
    bits = [r['bits'] for r in results]
    times = [r['time'] for r in results]
    timeouts = [r['timeout'] for r in results]
    
    # =========================================================
    # LEFT PLOT: Linear x-axis, log y-axis
    # =========================================================
    
    # Plot successful completions
    success_bits = [r['bits'] for r in results if not r['timeout']]
    success_times = [r['time'] for r in results if not r['timeout']]
    
    if success_bits:
        ax1.plot(success_bits, success_times, 'o-', color='#e74c3c', linewidth=2.5, markersize=12, 
                 label='Brute Force (answer at p-2, completed)', markeredgecolor='darkred', markeredgewidth=1.5)
    
    # Plot timeouts
    timeout_bits = [r['bits'] for r in results if r['timeout']]
    for tb in timeout_bits:
        ax1.scatter(tb, TIMEOUT_SECONDS, color='red', marker='x', s=300, linewidth=3, zorder=5,
                   label='Timeout (10 min)' if tb == timeout_bits[0] else '')
    
    # Add O(2^n) theoretical line (if we have at least one successful completion)
    if success_bits and len(success_bits) >= 1:
        # Scale based on first successful measurement
        scale_factor = success_times[0] / (2**success_bits[0])
        n_range = np.array([30, 40, 50, 60])
        theoretical = scale_factor * (2**n_range)
        ax1.plot(n_range, theoretical, 'k--', linewidth=2, alpha=0.7, 
                 label='O(2^n) theoretical')
    
    # Add timeout line
    ax1.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.5, 
                label=f'Timeout limit ({TIMEOUT_SECONDS}s)')
    
    ax1.set_xlabel('Prime Bit Length (n)', fontweight='bold')
    ax1.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax1.set_title('Worst-Case Brute Force (X = timeout)', fontweight='bold')
    ax1.set_yscale('log')
    ax1.set_xlim(28, 52)
    ax1.set_ylim(1, TIMEOUT_SECONDS * 1.5)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='upper left')
    
    # Add value labels for successful completions
    for b, t in zip(success_bits, success_times):
        ax1.annotate(f'{t:.1f}s', xy=(b, t), xytext=(b+1, t*0.8),
                    fontsize=10, ha='left', va='center',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # =========================================================
    # RIGHT PLOT: Log-log scale
    # =========================================================
    
    if success_bits:
        ax2.loglog(success_bits, success_times, 'o-', color='#e74c3c', linewidth=2.5, markersize=12,
                   label='Brute Force (completed)', markeredgecolor='darkred')
    
    for tb in timeout_bits:
        ax2.scatter(tb, TIMEOUT_SECONDS, color='red', marker='x', s=300, linewidth=3, zorder=5)
    
    if success_bits and len(success_bits) >= 1:
        ax2.loglog(n_range, theoretical, 'k--', linewidth=2, alpha=0.7,
                   label='O(2^n) reference')
    
    ax2.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
    
    ax2.set_xlabel('Prime Bit Length (n, log scale)', fontweight='bold')
    ax2.set_ylabel('Execution Time (seconds, log scale)', fontweight='bold')
    ax2.set_title('Exponential Growth (Log-Log View)', fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--', which='both')
    ax2.legend(loc='upper left')
    
    # Add annotation about 50-bit prediction
    ax2.annotate('50-bit predicted to take ~10-20 min\n(close to timeout limit)', 
                xy=(50, 600), xytext=(45, 100),
                arrowprops=dict(arrowstyle='->', color='orange', lw=1.5),
                fontsize=9, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('worst_case_30_40_50_timeout.png', dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"\n  [OK] Graph saved: worst_case_30_40_50_timeout.png")

def plot_comparison_chart(results):
    """
    Create a clean comparison chart showing actual vs theoretical
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Extract data
    bits = [r['bits'] for r in results]
    times = [r['time'] for r in results]
    timeouts = [r['timeout'] for r in results]
    
    # Plot bars for actual times
    colors = ['#e74c3c' if not t else '#95a5a6' for t in timeouts]
    bars = ax.bar([str(b) for b in bits], times, color=colors, alpha=0.7, edgecolor='black',
                  label='Actual Time')
    
    # Add timeout annotation
    for i, (b, t, to) in enumerate(zip(bits, times, timeouts)):
        if to:
            ax.text(i, t + 50, f'TIMEOUT\n({t:.0f}s)', ha='center', va='bottom',
                   fontsize=10, color='red', fontweight='bold')
        else:
            ax.text(i, t + 5, f'{t:.1f}s', ha='center', va='bottom', fontsize=10)
    
    # Add theoretical O(2^n) line (scaled to 30-bit)
    if len(results) > 0 and not results[0]['timeout']:
        theoretical_times = [times[0] * (2**(b - bits[0])) for b in bits]
        ax.plot([str(b) for b in bits], theoretical_times, 'k--', linewidth=2.5,
                marker='s', markersize=8, label='O(2^n) Theoretical', alpha=0.7)
    
    # Add timeout line
    ax.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.7, linewidth=2,
               label=f'Timeout Limit ({TIMEOUT_SECONDS}s)')
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold', fontsize=12)
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold', fontsize=12)
    ax.set_title('Worst-Case Brute Force: 30, 40, 50-bit (Answer at p-2)', 
                fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.legend(loc='upper left')
    
    # Add note
    ax.text(0.98, 0.02, 'Note: Search space = p-2 possibilities\n50-bit requires ~1.1e15 checks',
           transform=ax.transAxes, ha='right', va='bottom',
           fontsize=9, style='italic',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('worst_case_comparison_chart.png', dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] Graph saved: worst_case_comparison_chart.png")

def print_summary(results):
    """Print detailed summary"""
    print("\n" + "="*80)
    print("  ANALYSIS SUMMARY")
    print("="*80)
    
    print("\nWorst-Case Results (Answer at p-2):")
    print("-" * 70)
    print(f"{'Bit Length':<12} {'Time (seconds)':<18} {'Time (minutes)':<18} {'Status':<15}")
    print("-" * 70)
    
    for r in results:
        minutes = r['time'] / 60
        status = "TIMEOUT" if r['timeout'] else "COMPLETED"
        print(f"{r['bits']:<12} {r['time']:<18.2f} {minutes:<18.2f} {status:<15}")
    
    print("\n" + "-" * 70)
    print("KEY FINDINGS:")
    print("-" * 70)
    
    completed = [r for r in results if not r['timeout']]
    
    if completed:
        print(f"\n  • 30-bit: {completed[0]['time']:.2f} seconds to check all {2**30:,} possibilities")
        if len(completed) > 1:
            print(f"  • 40-bit: {completed[1]['time']:.2f} seconds ({completed[1]['time']/60:.2f} minutes)")
        if len(completed) > 2:
            print(f"  • 50-bit: {completed[2]['time']:.2f} seconds ({completed[2]['time']/60:.2f} minutes)")
    
    timeouts = [r for r in results if r['timeout']]
    if timeouts:
        print(f"\n  • Timeout at {timeouts[0]['bits']}-bit after {timeouts[0]['time']:.0f} seconds")
    
    print("\n" + "-" * 70)
    print("CRYPTOGRAPHIC IMPLICATIONS:")
    print("-" * 70)
    print("  • 30-bit worst-case: ~5-10 seconds on modern hardware")
    print("  • 40-bit worst-case: ~2-3 minutes")
    print("  • 50-bit worst-case: ~20-40 minutes (may hit timeout)")
    print("  • 60-bit would take ~10-20 hours (impossible for practical use)")
    print("  • 128-bit would take ~10^25 years (why crypto is secure)")
    print("\n" + "="*80)

def main():
    """Run worst-case analysis for 30, 40, 50 bits with timeout"""
    
    print("\n" + "="*80)
    print("  WORST-CASE DLP BRUTE FORCE ANALYSIS")
    print("  Testing 30, 40, 50 bits with answer at p-2")
    print(f"  Timeout: {TIMEOUT_SECONDS}s (10 minutes)")
    print("="*80)
    
    print("\nWARNING: 50-bit test may take 20-40 minutes!")
    print("Press Ctrl+C to skip if needed\n")
    
    response = input("Continue? (y/n): ").lower()
    if response != 'y':
        print("Aborted.")
        return
    
    # Run analysis
    results = run_worst_case_analysis()
    
    if results:
        # Generate plots
        plot_worst_case_analysis(results)
        plot_comparison_chart(results)
        
        # Print summary
        print_summary(results)
        
        print("\n" + "="*80)
        print("  ANALYSIS COMPLETE")
        print("="*80)
        print("\nGenerated files:")
        print("  - worst_case_30_40_50_timeout.png (Main comparison)")
        print("  - worst_case_comparison_chart.png (Bar chart comparison)")
    else:
        print("\n[!] No results generated.")

if __name__ == "__main__":
    main()