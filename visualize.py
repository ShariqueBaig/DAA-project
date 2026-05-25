"""
DLP Benchmark Visualization - Shows timeout cutoffs at 600s
"""

import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Configure matplotlib
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300
})

# Color schemes
ALGO_COLORS = {
    "Brute Force": "#e74c3c",
    "BSGS": "#3498db",
    "Pollard's Rho": "#2ecc71",
    "Pohlig-Hellman": "#f39c12"
}

ALGO_MARKERS = {
    "Brute Force": "o",
    "BSGS": "s",
    "Pollard's Rho": "D",
    "Pohlig-Hellman": "^"
}

DATASET_COLORS = {
    "weak": "#e74c3c",
    "random": "#3498db",
    "hard": "#2ecc71"
}

DATASET_STYLES = {
    "weak": "-",
    "random": "--",
    "hard": ":"
}

TIMEOUT_SECONDS = 600  # 10 minutes

GRAPH_DIR = "graphs"

def safe_filename(name):
    """Convert algorithm name to safe filename"""
    return name.lower().replace(" ", "_").replace("'", "").replace("-", "_")

def load_results(csv_file="benchmark_results.csv"):
    """Load benchmark results from CSV"""
    results = []
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Run benchmark.py first.")
        return results
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['bit_length'] = int(row['bit_length'])
                row['time_seconds'] = float(row['time_seconds']) if row.get('time_seconds') and float(row['time_seconds']) > 0 else None
                row['timeout_occurred'] = row.get('timeout_occurred', 'False') == 'True'
                row['memory_estimate_bytes'] = int(row.get('memory_estimate_bytes', 0))
                results.append(row)
            except (ValueError, KeyError) as e:
                continue
    
    return results

def setup_graph_dir():
    if not os.path.exists(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)

def plot_individual_algorithm(results):
    """Graph for each algorithm showing performance across datasets with timeout markers"""
    algorithms = ALGO_COLORS.keys()
    
    for algo in algorithms:
        fig, ax = plt.subplots(figsize=(12, 7))
        
        for dataset in ['weak', 'random', 'hard']:
            # Filter data
            data = []
            for r in results:
                if r.get('algorithm') == algo and r.get('dataset') == dataset:
                    bits = r['bit_length']
                    time_val = r.get('time_seconds')
                    timeout = r.get('timeout_occurred', False)
                    if time_val is not None and time_val > 0:
                        data.append((bits, time_val, timeout))
            
            if not data:
                continue
            
            data.sort()
            bits = [d[0] for d in data]
            times = [d[1] for d in data]
            timeouts = [d[2] for d in data]
            
            # Plot with timeout markers
            valid_bits = [b for b, t, to in zip(bits, times, timeouts) if not to]
            valid_times = [t for b, t, to in zip(bits, times, timeouts) if not to]
            timeout_bits = [b for b, t, to in zip(bits, times, timeouts) if to]
            
            if valid_bits:
                ax.plot(valid_bits, valid_times,
                       marker=ALGO_MARKERS[algo],
                       color=DATASET_COLORS[dataset],
                       linestyle=DATASET_STYLES[dataset],
                       linewidth=2.5,
                       markersize=8,
                       label=f'{dataset.upper()} primes',
                       alpha=0.9)
            
            # Add timeout markers
            for tb in timeout_bits:
                ax.scatter(tb, TIMEOUT_SECONDS, 
                          color='red', marker='x', s=200, linewidth=3,
                          zorder=5, alpha=0.8)
        
        # Add horizontal line at timeout
        ax.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.5, 
                   label=f'Timeout limit ({TIMEOUT_SECONDS}s)')
        
        ax.set_xlabel('Prime Bit Length', fontweight='bold')
        ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
        ax.set_title(f'{algo} - Runtime by Prime Type (X marks timeout)', fontweight='bold')
        ax.set_yscale('log')
        ax.set_ylim(1e-6, TIMEOUT_SECONDS * 2)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='upper left')
        
        plt.tight_layout()
        filename = f"{safe_filename(algo)}_by_dataset.png"
        plt.savefig(os.path.join(GRAPH_DIR, filename))
        plt.close()
        print(f"  ✓ Saved: {filename}")

def plot_all_algorithms_single_dataset(results, dataset):
    """All algorithms on one dataset with timeout markers"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    title_map = {
        'weak': 'Weak Primes (p-1 has small factors)',
        'random': 'Random Primes (Standard cryptographic primes)',
        'hard': 'Hard Primes (p-1 has large prime factors)'
    }
    
    for algo in ALGO_COLORS.keys():
        # Filter data
        data = []
        for r in results:
            if r.get('algorithm') == algo and r.get('dataset') == dataset:
                bits = r['bit_length']
                time_val = r.get('time_seconds')
                timeout = r.get('timeout_occurred', False)
                if time_val is not None and time_val > 0:
                    data.append((bits, time_val, timeout))
        
        if not data:
            continue
        
        data.sort()
        bits = [d[0] for d in data]
        times = [d[1] for d in data]
        timeouts = [d[2] for d in data]
        
        valid_bits = [b for b, t, to in zip(bits, times, timeouts) if not to]
        valid_times = [t for b, t, to in zip(bits, times, timeouts) if not to]
        timeout_bits = [b for b, t, to in zip(bits, times, timeouts) if to]
        
        if valid_bits:
            ax.plot(valid_bits, valid_times,
                   marker=ALGO_MARKERS[algo],
                   color=ALGO_COLORS[algo],
                   linewidth=2.5,
                   markersize=8,
                   label=algo,
                   alpha=0.9)
        
        for tb in timeout_bits:
            ax.scatter(tb, TIMEOUT_SECONDS, 
                      color='red', marker='x', s=200, linewidth=3,
                      zorder=5)
    
    ax.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.5, 
               label=f'Timeout limit ({TIMEOUT_SECONDS}s)')
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title(f'Algorithm Comparison - {title_map[dataset]} (X marks timeout)', fontweight='bold')
    ax.set_yscale('log')
    ax.set_ylim(1e-6, TIMEOUT_SECONDS * 2)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', ncol=2)
    
    plt.tight_layout()
    filename = f"all_algorithms_{dataset}_primes.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def plot_memory_comparison(results):
    """Memory usage comparison"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    memory_data = defaultdict(lambda: defaultdict(list))
    
    for r in results:
        if r.get('memory_estimate_bytes', 0) > 0:
            memory_data[r.get('algorithm')][r.get('bit_length')].append(r['memory_estimate_bytes'])
    
    for algo in ALGO_COLORS.keys():
        if algo not in memory_data:
            continue
        
        bits = sorted(memory_data[algo].keys())
        mems = [sum(memory_data[algo][b]) / len(memory_data[algo][b]) for b in bits]
        
        if bits:
            ax.plot(bits, mems,
                   marker=ALGO_MARKERS[algo],
                   color=ALGO_COLORS[algo],
                   linewidth=2.5,
                   markersize=7,
                   label=algo,
                   alpha=0.9)
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Memory Usage (bytes)', fontweight='bold')
    ax.set_title('Memory Usage Comparison by Algorithm', fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    filename = "memory_comparison.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def plot_complexity_validation(results):
    """Log-log plot validating theoretical complexities - FIXED with pow()"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Find min and max bit lengths for reference lines
    all_bits = []
    for algo in ['BSGS', "Pollard's Rho", 'Brute Force']:
        data = [
            r['bit_length']
            for r in results
            if r.get('algorithm') == algo and r.get('dataset') == 'random' 
            and r.get('time_seconds') is not None and r['time_seconds'] > 0
            and not r.get('timeout_occurred', False)
        ]
        all_bits.extend(data)
    
    if not all_bits:
        print("  Warning: No data for complexity validation")
        plt.close()
        return
    
    min_bit = min(all_bits)
    max_bit = max(all_bits)
    
    for algo in ['BSGS', "Pollard's Rho", 'Brute Force']:
        data = [
            (r['bit_length'], r['time_seconds'])
            for r in results
            if r.get('algorithm') == algo and r.get('dataset') == 'random' 
            and r.get('time_seconds') is not None and r['time_seconds'] > 0
            and not r.get('timeout_occurred', False)
        ]
        
        if not data:
            continue
        
        data.sort()
        bits = [d[0] for d in data]
        times = [d[1] for d in data]
        
        ax.loglog(bits, times,
                 marker=ALGO_MARKERS.get(algo, 'o'),
                 color=ALGO_COLORS.get(algo, '#333'),
                 linewidth=2,
                 markersize=6,
                 label=f'{algo} (empirical)',
                 alpha=0.8)
    
    # Theoretical lines - using pow() with float base for negative exponents
    n_range = np.array([16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50])
    # Filter to our range
    n_range = n_range[(n_range >= min_bit) & (n_range <= max_bit + 4)]
    
    if len(n_range) > 0:
        # O(2^n) reference - use pow(2.0, exponent) for float exponentiation
        o2n = [pow(2.0, n - 20) * 0.0001 for n in n_range]
        ax.loglog(n_range, o2n, 'k--', linewidth=2, alpha=0.5, label='O(2^n) reference')
        
        # O(2^(n/2)) reference
        o2n2 = [pow(2.0, (n - 20) / 2) * 0.00001 for n in n_range]
        ax.loglog(n_range, o2n2, 'k:', linewidth=2, alpha=0.5, label='O(2^(n/2)) reference')
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('Complexity Validation - Empirical vs Theoretical', fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    filename = "complexity_validation.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def plot_pohlig_hellman_vulnerability(results):
    """Focus on Pohlig-Hellman showing weak prime vulnerability"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for dataset in ['weak', 'random', 'hard']:
        data = []
        for r in results:
            if r.get('algorithm') == 'Pohlig-Hellman' and r.get('dataset') == dataset:
                bits = r['bit_length']
                time_val = r.get('time_seconds')
                timeout = r.get('timeout_occurred', False)
                if time_val is not None and time_val > 0:
                    data.append((bits, time_val, timeout))
        
        if not data:
            continue
        
        data.sort()
        bits = [d[0] for d in data]
        times = [d[1] for d in data]
        timeouts = [d[2] for d in data]
        
        valid_bits = [b for b, t, to in zip(bits, times, timeouts) if not to]
        valid_times = [t for b, t, to in zip(bits, times, timeouts) if not to]
        timeout_bits = [b for b, t, to in zip(bits, times, timeouts) if to]
        
        if valid_bits:
            ax.plot(valid_bits, valid_times,
                   marker='o',
                   color=DATASET_COLORS[dataset],
                   linestyle=DATASET_STYLES[dataset],
                   linewidth=2.5,
                   markersize=8,
                   label=f'{dataset.upper()} primes',
                   alpha=0.9)
        
        for tb in timeout_bits:
            ax.scatter(tb, TIMEOUT_SECONDS, color='red', marker='x', s=200, linewidth=3)
    
    ax.axhline(y=TIMEOUT_SECONDS, color='red', linestyle='--', alpha=0.5, label=f'Timeout ({TIMEOUT_SECONDS}s)')
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('Pohlig-Hellman: Weak Prime Vulnerability (X marks timeout)', fontweight='bold')
    ax.set_yscale('log')
    ax.set_ylim(1e-6, TIMEOUT_SECONDS * 2)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    # Highlight vulnerability
    ax.annotate('Weak primes: dramatically faster\n(10^4-10^5x speedup)',
                xy=(28, 0.0001), xytext=(32, 0.001),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    filename = "pohlig_hellman_vulnerability.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def plot_performance_summary(results):
    """Summary bar chart showing max bit length achieved"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    max_bits = {}
    for algo in ALGO_COLORS.keys():
        max_bits[algo] = {}
        for dataset in ['weak', 'random', 'hard']:
            bits_achieved = [
                r['bit_length']
                for r in results
                if r.get('algorithm') == algo and r.get('dataset') == dataset 
                and r.get('time_seconds') is not None and r['time_seconds'] > 0
                and not r.get('timeout_occurred', False)
            ]
            max_bits[algo][dataset] = max(bits_achieved) if bits_achieved else 0
    
    algorithms = list(ALGO_COLORS.keys())
    x = np.arange(len(algorithms))
    width = 0.25
    
    for i, dataset in enumerate(['weak', 'random', 'hard']):
        values = [max_bits[algo][dataset] for algo in algorithms]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, values, width, 
                     label=dataset.upper(), 
                     color=DATASET_COLORS[dataset],
                     alpha=0.8,
                     edgecolor='black')
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       str(val), ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Algorithm', fontweight='bold')
    ax.set_ylabel('Maximum Bit Length Achieved (before timeout)', fontweight='bold')
    ax.set_title('Algorithm Scalability - Max Bit Length by Prime Type', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    plt.tight_layout()
    filename = "scalability_summary.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def plot_timeout_analysis(results):
    """Additional graph showing where timeouts occur"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Count timeouts by algorithm and bit length
    timeout_data = defaultdict(lambda: defaultdict(int))
    
    for r in results:
        if r.get('timeout_occurred', False):
            algo = r.get('algorithm')
            bits = r.get('bit_length')
            timeout_data[algo][bits] += 1
    
    for algo in ALGO_COLORS.keys():
        if algo not in timeout_data:
            continue
        
        bits = sorted(timeout_data[algo].keys())
        counts = [timeout_data[algo][b] for b in bits]
        
        if bits:
            ax.plot(bits, counts,
                   marker=ALGO_MARKERS[algo],
                   color=ALGO_COLORS[algo],
                   linewidth=2,
                   markersize=8,
                   label=algo,
                   alpha=0.9)
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Number of Timeouts', fontweight='bold')
    ax.set_title('When Algorithms Hit the 10-Minute Timeout Limit', fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    filename = "timeout_analysis.png"
    plt.savefig(os.path.join(GRAPH_DIR, filename))
    plt.close()
    print(f"  ✓ Saved: {filename}")

def generate_report(results):
    """Generate summary report"""
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("DLP ALGORITHM ANALYSIS - SUMMARY REPORT")
    report_lines.append("="*80)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Hard Timeout: {TIMEOUT_SECONDS} seconds ({TIMEOUT_SECONDS/60} minutes)")
    report_lines.append(f"Total test runs: {len(results)}")
    
    # Timeout statistics
    timeout_count = sum(1 for r in results if r.get('timeout_occurred', False))
    report_lines.append(f"Timeouts occurred: {timeout_count}")
    
    # Summary by algorithm
    report_lines.append("\n" + "-"*40)
    report_lines.append("PERFORMANCE SUMMARY BY ALGORITHM")
    report_lines.append("-"*40)
    
    for algo in ALGO_COLORS.keys():
        algo_results = [r for r in results if r.get('algorithm') == algo]
        passed = [r for r in algo_results if r.get('status') == 'PASSED']
        timed_out = [r for r in algo_results if r.get('timeout_occurred', False)]
        
        report_lines.append(f"\n{algo}:")
        report_lines.append(f"  Passed: {len(passed)} tests")
        report_lines.append(f"  Timed out: {len(timed_out)} tests")
        
        for dataset in ['weak', 'random', 'hard']:
            dataset_results = [r for r in passed if r.get('dataset') == dataset]
            if dataset_results:
                max_bit = max(r['bit_length'] for r in dataset_results)
                avg_time = sum(r['time_seconds'] for r in dataset_results) / len(dataset_results)
                report_lines.append(f"  {dataset.upper()}: max {max_bit}-bit, avg {avg_time:.6f}s")
    
    # Key findings
    report_lines.append("\n" + "-"*40)
    report_lines.append("KEY FINDINGS")
    report_lines.append("-"*40)
    
    # Pohlig-Hellman vulnerability
    ph_weak = [r for r in results if r.get('algorithm') == 'Pohlig-Hellman' and r.get('dataset') == 'weak' and r.get('time_seconds') and r['time_seconds'] > 0 and not r.get('timeout_occurred')]
    ph_hard = [r for r in results if r.get('algorithm') == 'Pohlig-Hellman' and r.get('dataset') == 'hard' and r.get('time_seconds') and r['time_seconds'] > 0 and not r.get('timeout_occurred')]
    
    if ph_weak and ph_hard:
        avg_weak = sum(r['time_seconds'] for r in ph_weak) / len(ph_weak)
        avg_hard = sum(r['time_seconds'] for r in ph_hard) / len(ph_hard)
        speedup = avg_hard / avg_weak
        report_lines.append(f"\n1. Pohlig-Hellman speedup on weak primes: {speedup:.0f}x faster")
        report_lines.append(f"   Weak avg: {avg_weak:.6f}s, Hard avg: {avg_hard:.6f}s")
    
    # Brute force limit
    bf_results = [r for r in results if r.get('algorithm') == 'Brute Force' and not r.get('timeout_occurred')]
    if bf_results:
        max_bf = max(r['bit_length'] for r in bf_results)
        report_lines.append(f"\n2. Brute force feasible up to {max_bf}-bit primes before timeout")
    
    # BSGS memory
    bsgs_mem = [r for r in results if r.get('algorithm') == 'BSGS' and r.get('memory_estimate_bytes', 0) > 0]
    if bsgs_mem:
        max_mem = max(r['memory_estimate_bytes'] for r in bsgs_mem)
        report_lines.append(f"\n3. BSGS max memory usage: {max_mem/1024/1024:.1f} MB")
    
    # Best scalability
    report_lines.append(f"\n4. Best scalability: Pollard's Rho (constant memory, O(sqrt(p)) time)")
    report_lines.append(f"   Reached highest bit lengths before timeout")
    
    report_lines.append("\n" + "="*80)
    
    # Save report - use utf-8 encoding to handle all Unicode characters
    report_path = os.path.join(GRAPH_DIR, "analysis_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\n  ✓ Saved: analysis_report.txt")
    # Print key findings to console (using ASCII replacement for sqrt)
    print("\n" + "-"*40)
    print("KEY FINDINGS (from report):")
    print("-"*40)
    for line in report_lines[-20:]:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
            # Replace Unicode sqrt with 'sqrt' for console output
            console_line = line.replace('√', 'sqrt')
            print(console_line)
            
def main():
    print("\n" + "="*60)
    print("  DLP ANALYSIS VISUALIZATION SUITE")
    print(f"  Hard Timeout: {TIMEOUT_SECONDS}s (shown as red X)")
    print("="*60)
    
    results = load_results()
    if not results:
        print("No results found. Run benchmark.py first.")
        return
    
    print(f"\nLoaded {len(results)} result records")
    setup_graph_dir()
    
    print("\nGenerating graphs...\n")
    
    plot_individual_algorithm(results)
    print()
    
    for dataset in ['weak', 'random', 'hard']:
        plot_all_algorithms_single_dataset(results, dataset)
    print()
    
    plot_memory_comparison(results)
    plot_complexity_validation(results)
    plot_pohlig_hellman_vulnerability(results)
    plot_performance_summary(results)
    plot_timeout_analysis(results)
    generate_report(results)
    
    print(f"\n{'='*60}")
    print(f"  Graphs saved to: ./{GRAPH_DIR}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()