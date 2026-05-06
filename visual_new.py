"""
Complete DLP Visualization with Hardcoded Data
All data extracted from benchmark_results.csv
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Configure matplotlib for publication quality
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'figure.figsize': (12, 7)
})

# Color schemes
ALGO_COLORS = {
    "Brute Force": "#e74c3c",      # Red
    "BSGS": "#3498db",              # Blue
    "Pollard's Rho": "#2ecc71",     # Green
    "Pohlig-Hellman": "#f39c12"     # Orange
}

ALGO_MARKERS = {
    "Brute Force": "o",
    "BSGS": "s",
    "Pollard's Rho": "D",
    "Pohlig-Hellman": "^"
}

ALGO_LINESTYLES = {
    "Brute Force": "-",
    "BSGS": "--",
    "Pollard's Rho": "-.",
    "Pohlig-Hellman": ":"
}

DATASET_COLORS = {
    "weak": "#e74c3c",
    "random": "#3498db",
    "hard": "#2ecc71"
}

DATASET_NAMES = {
    "weak": "Weak Primes (p-1 smooth)",
    "random": "Random Primes",
    "hard": "Hard Primes (p = 2q+1)"
}

# ============================================================================
# HARDCODED DATA FROM BENCHMARK (all algorithms, up to bits where BF completed)
# ============================================================================

# Brute Force - from your selective benchmark (new data)
BRUTE_FORCE_DATA = {
    (16, "weak"): 0.05, (16, "random"): 0.02, (16, "hard"): 0.02,
    (18, "weak"): 0.09, (18, "random"): 0.13, (18, "hard"): 0.11,
    (20, "weak"): 0.40, (20, "random"): 0.72, (20, "hard"): 0.68,
    (22, "weak"): 2.92, (22, "random"): 2.90, (22, "hard"): 4.00,
    (24, "weak"): 14.47, (24, "random"): 9.64, (24, "hard"): 13.93,
    (26, "weak"): 55.05, (26, "random"): 119.68, (26, "hard"): 36.25,
    (28, "weak"): 250.07, (28, "random"): 174.87, (28, "hard"): 155.27,
}

# Pohlig-Hellman - from your selective benchmark (new data)
POHLIG_HELLMAN_DATA = {
    (16, "weak"): 0.001, (16, "random"): 0.001, (16, "hard"): 0.01,
    (18, "weak"): 0.001, (18, "random"): 0.001, (18, "hard"): 0.04,
    (20, "weak"): 0.001, (20, "random"): 0.06, (20, "hard"): 0.20,
    (22, "weak"): 0.001, (22, "random"): 0.001, (22, "hard"): 1.56,
    (24, "weak"): 0.001, (24, "random"): 0.001, (24, "hard"): 4.55,
    (26, "weak"): 0.001, (26, "random"): 0.01, (26, "hard"): 11.44,
    (28, "weak"): 0.001, (28, "random"): 0.001, (28, "hard"): 72.89,
}

# BSGS - from benchmark_results.csv (existing data)
BSGS_DATA = {
    (16, "weak"): 0.0022, (16, "random"): 0.0001, (16, "hard"): 0.00013,
    (18, "weak"): 0.00027, (18, "random"): 0.00018, (18, "hard"): 0.00017,
    (20, "weak"): 0.00039, (20, "random"): 0.00028, (20, "hard"): 0.00077,
    (22, "weak"): 0.00079, (22, "random"): 0.00059, (22, "hard"): 0.00084,
    (24, "weak"): 0.00113, (24, "random"): 0.00115, (24, "hard"): 0.00184,
    (26, "weak"): 0.00197, (26, "random"): 0.00160, (26, "hard"): 0.00222,
    (28, "weak"): 0.00330, (28, "random"): 0.00363, (28, "hard"): 0.00388,
    (30, "weak"): 0.00735, (30, "random"): 0.00925, (30, "hard"): 0.00767,
    (32, "weak"): 0.0187, (32, "random"): 0.0204, (32, "hard"): 0.0206,
    (34, "weak"): 0.0394, (34, "random"): 0.0556, (34, "hard"): 0.0534,
    (36, "weak"): 0.0821, (36, "random"): 0.0995, (36, "hard"): 0.0975,
    (38, "weak"): 0.176, (38, "random"): 0.183, (38, "hard"): 0.162,
    (40, "weak"): 0.352, (40, "random"): 0.422, (40, "hard"): 0.461,
    (42, "weak"): 0.801, (42, "random"): 0.930, (42, "hard"): 1.023,
    (44, "weak"): 2.100, (44, "random"): 1.856, (44, "hard"): 2.245,
    (46, "weak"): 3.978, (46, "random"): 5.601, (46, "hard"): 4.653,
    (48, "weak"): 11.10, (48, "random"): 8.850, (48, "hard"): 10.02,
    (50, "weak"): 19.37, (50, "random"): 19.42, (50, "hard"): 24.58,
    (52, "weak"): 52.58, (52, "random"): 46.42, (52, "hard"): 46.75,
    (54, "weak"): 112.9, (54, "random"): 231.2, (54, "hard"): 234.5,
}

# Pollard's Rho - from benchmark_results.csv (existing data)
POLLARDS_RHO_DATA = {
    (16, "weak"): 0.00051, (16, "random"): 0.00027, (16, "hard"): 0.00040,
    (18, "weak"): 0.00085, (18, "random"): 0.00038, (18, "hard"): 0.00028,
    (20, "weak"): 0.00030, (20, "random"): 0.00071, (20, "hard"): 0.00119,
    (22, "weak"): 0.00221, (22, "random"): 0.00130, (22, "hard"): 0.00178,
    (24, "weak"): 0.00191, (24, "random"): 0.00169, (24, "hard"): 0.00221,
    (26, "weak"): 0.00335, (26, "random"): 0.00941, (26, "hard"): 0.0132,
    (28, "weak"): 0.00916, (28, "random"): 0.00609, (28, "hard"): 0.0113,
    (30, "weak"): 0.0330, (30, "random"): 0.0680, (30, "hard"): 0.0381,
    (32, "weak"): 0.1495, (32, "random"): 0.1074, (32, "hard"): 0.1030,
    (34, "weak"): 0.0948, (34, "random"): 0.3861, (34, "hard"): 0.3952,
    (36, "weak"): 0.3037, (36, "random"): 0.5539, (36, "hard"): 0.6110,
    (38, "weak"): 1.231, (38, "random"): 0.4854, (38, "hard"): 1.237,
    (40, "weak"): 3.127, (40, "random"): 1.386, (40, "hard"): 1.211,
    (42, "weak"): 3.700, (42, "random"): 0.9666, (42, "hard"): 2.269,
    (44, "weak"): 5.691, (44, "random"): 5.314, (44, "hard"): 4.531,
    (46, "weak"): 7.278, (46, "random"): 13.50, (46, "hard"): 5.643,
    (48, "weak"): 29.74, (48, "random"): 51.83, (48, "hard"): 10.99,
    (50, "weak"): 34.13, (50, "random"): 36.45, (50, "hard"): 21.08,
    (52, "weak"): 74.34, (52, "random"): 44.42, (52, "hard"): 146.1,
    (54, "weak"): 261.6, (54, "random"): 316.0, (54, "hard"): 237.5,
}

# Combine all data
ALL_DATA = {
    "Brute Force": BRUTE_FORCE_DATA,
    "BSGS": BSGS_DATA,
    "Pollard's Rho": POLLARDS_RHO_DATA,
    "Pohlig-Hellman": POHLIG_HELLMAN_DATA,
}

def plot_individual_algorithm(algo_name, data):
    """Plot single algorithm performance across datasets"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algo_data = data.get(algo_name, {})
    if not algo_data:
        print(f"No data for {algo_name}")
        return
    
    for dataset in ['weak', 'random', 'hard']:
        points = [(bits, time) for (bits, ds), time in algo_data.items() if ds == dataset]
        if points:
            points.sort()
            bits = [p[0] for p in points]
            times = [p[1] for p in points]
            
            # Replace 0 times with a small value for log scale
            times = [max(t, 1e-6) for t in times]
            
            ax.plot(bits, times, 
                   marker=ALGO_MARKERS[algo_name],
                   color=DATASET_COLORS[dataset],
                   linestyle='-',
                   linewidth=2.5,
                   markersize=8,
                   label=f'{dataset.upper()} primes',
                   alpha=0.9)
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title(f'{algo_name} Performance by Prime Type', fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.set_ylim(1e-6, 1000)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    # Add complexity reference for Brute Force
    if algo_name == "Brute Force":
        n_range = np.array([16, 18, 20, 22, 24, 26, 28])
        scale = 0.5 / (2**20)
        theoretical = scale * (2**n_range)
        ax.plot(n_range, theoretical, 'k--', linewidth=1.5, alpha=0.5, 
               label='O(2ⁿ) reference')
    
    plt.tight_layout()
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/{algo_name.lower().replace(" ", "_")}_performance.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {algo_name.lower().replace(' ', '_')}_performance.png")

def plot_all_algorithms_comparison(data, dataset):
    """Plot all algorithms on a single dataset"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for algo_name in ALGO_COLORS.keys():
        algo_data = data.get(algo_name, {})
        points = [(bits, time) for (bits, ds), time in algo_data.items() if ds == dataset]
        
        if points:
            points.sort()
            bits = [p[0] for p in points]
            times = [p[1] for p in points]
            times = [max(t, 1e-6) for t in times]
            
            ax.plot(bits, times,
                   marker=ALGO_MARKERS[algo_name],
                   color=ALGO_COLORS[algo_name],
                   linestyle=ALGO_LINESTYLES[algo_name],
                   linewidth=2.5,
                   markersize=8,
                   label=algo_name,
                   alpha=0.9)
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title(f'Algorithm Comparison - {DATASET_NAMES[dataset]}', fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.set_ylim(1e-6, 1000)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', ncol=2)
    
    # Add theoretical reference lines (using float exponentiation)
    n_range = np.array([16, 20, 24, 28, 32, 36, 40, 44, 48, 52])
    
    # O(2^n) reference - use pow(2.0, exponent) to handle negative exponents
    o2n = [pow(2.0, n - 20) * 0.001 for n in n_range]
    ax.plot(n_range, o2n, 'k--', linewidth=1.5, alpha=0.4, label='O(2ⁿ) reference')
    
    # O(2^(n/2)) reference
    o2n2 = [pow(2.0, (n - 20) / 2) * 0.0001 for n in n_range]
    ax.plot(n_range, o2n2, 'k:', linewidth=1.5, alpha=0.4, label='O(√(2ⁿ)) reference')
    
    plt.tight_layout()
    filename = f'graphs/all_algorithms_{dataset}_primes.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: all_algorithms_{dataset}_primes.png")

def plot_pohlig_hellman_vulnerability(data):
    """Special plot showing PH vulnerability on weak primes"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ph_data = data.get("Pohlig-Hellman", {})
    
    for dataset in ['weak', 'random', 'hard']:
        points = [(bits, time) for (bits, ds), time in ph_data.items() if ds == dataset]
        if points:
            points.sort()
            bits = [p[0] for p in points]
            times = [p[1] for p in points]
            times = [max(t, 1e-6) for t in times]
            
            ax.plot(bits, times,
                   marker='o',
                   color=DATASET_COLORS[dataset],
                   linestyle='-',
                   linewidth=2.5,
                   markersize=8,
                   label=f'{dataset.upper()} primes',
                   alpha=0.9)
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('Pohlig-Hellman: Weak Prime Vulnerability', fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.set_ylim(1e-6, 100)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    # Highlight the vulnerability
    ax.annotate('Weak primes: extremely fast\n(p-1 has only small factors)',
                xy=(24, 0.001), xytext=(26, 0.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax.annotate('Hard primes: much slower\n(p = 2q+1 safe prime)',
                xy=(26, 11.44), xytext=(20, 30),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
                fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    filename = 'graphs/pohlig_hellman_vulnerability.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: pohlig_hellman_vulnerability.png")

def plot_brute_force_growth(data):
    """Plot Brute Force growth with O(2^n) reference"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bf_data = data.get("Brute Force", {})
    
    for dataset in ['weak', 'random', 'hard']:
        points = [(bits, time) for (bits, ds), time in bf_data.items() if ds == dataset]
        if points:
            points.sort()
            bits = [p[0] for p in points]
            times = [p[1] for p in points]
            
            ax.plot(bits, times,
                   marker=ALGO_MARKERS["Brute Force"],
                   color=DATASET_COLORS[dataset],
                   linestyle='-',
                   linewidth=2.5,
                   markersize=8,
                   label=f'{dataset.upper()} primes',
                   alpha=0.9)
    
    # Add O(2^n) reference
    n_range = np.array([16, 18, 20, 22, 24, 26, 28])
    scale = 0.5 / (2**20)
    theoretical = scale * (2**n_range)
    ax.plot(n_range, theoretical, 'k--', linewidth=2, alpha=0.6, 
           label='O(2ⁿ) theoretical (scaled)')
    
    # Add annotations for growth on hard primes
    points_hard = [(bits, time) for (bits, ds), time in bf_data.items() if ds == "hard"]
    points_hard.sort()
    for i in range(1, len(points_hard)):
        bits_i, time_i = points_hard[i]
        bits_prev, time_prev = points_hard[i-1]
        ratio = time_i / time_prev
        ax.annotate(f'{ratio:.1f}x', 
                   xy=(bits_i, time_i),
                   xytext=(bits_i+0.5, time_i*0.7),
                   fontsize=9, ha='left',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    ax.set_xlabel('Prime Bit Length', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('Brute Force: Exponential Growth', fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    filename = 'graphs/brute_force_exponential_growth.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: brute_force_exponential_growth.png")

def plot_performance_summary(data):
    """Create a summary bar chart at 28 bits"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    algorithms = []
    weak_times = []
    random_times = []
    hard_times = []
    
    for algo_name in ALGO_COLORS.keys():
        algo_data = data.get(algo_name, {})
        
        weak_time = algo_data.get((28, "weak"), 0)
        random_time = algo_data.get((28, "random"), 0)
        hard_time = algo_data.get((28, "hard"), 0)
        
        if weak_time > 0 or random_time > 0 or hard_time > 0:
            algorithms.append(algo_name)
            weak_times.append(weak_time if weak_time > 0 else 1e-6)
            random_times.append(random_time if random_time > 0 else 1e-6)
            hard_times.append(hard_time if hard_time > 0 else 1e-6)
    
    x = np.arange(len(algorithms))
    width = 0.25
    
    bars1 = ax.bar(x - width, weak_times, width, label='Weak Primes', color='#e74c3c', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x, random_times, width, label='Random Primes', color='#3498db', alpha=0.8, edgecolor='black')
    bars3 = ax.bar(x + width, hard_times, width, label='Hard Primes', color='#2ecc71', alpha=0.8, edgecolor='black')
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height < 60:
                label = f'{height:.1f}s'
            else:
                label = f'{height/60:.1f}m'
            ax.text(bar.get_x() + bar.get_width()/2, height + 5, label,
                   ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Algorithm', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('28-bit Prime Performance Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.set_yscale('log')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    plt.tight_layout()
    filename = 'graphs/performance_summary_28bit.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: performance_summary_28bit.png")

def plot_complexity_comparison(data):
    """Plot all algorithms together to show complexity differences"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot each algorithm (use random primes as baseline)
    for algo_name in ALGO_COLORS.keys():
        algo_data = data.get(algo_name, {})
        points = [(bits, time) for (bits, ds), time in algo_data.items() if ds == "random"]
        
        if points:
            points.sort()
            bits = [p[0] for p in points]
            times = [p[1] for p in points]
            times = [max(t, 1e-6) for t in times]
            
            ax.plot(bits, times,
                   marker=ALGO_MARKERS[algo_name],
                   color=ALGO_COLORS[algo_name],
                   linestyle=ALGO_LINESTYLES[algo_name],
                   linewidth=2.5,
                   markersize=8,
                   label=algo_name,
                   alpha=0.9)
    
    # Add theoretical curves - using pow(2.0, exponent) for safe exponentiation
    n_range = np.array([16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56])
    
    # O(2^n) - Exponential (using float exponentiation)
    o2n = [pow(2.0, n - 20) * 0.0001 for n in n_range]
    ax.plot(n_range, o2n, 'k--', linewidth=2, alpha=0.5, label='O(2ⁿ) - Exponential')
    
    # O(2^(n/2)) - Sub-exponential
    o2n2 = [pow(2.0, (n - 20) / 2) * 0.00001 for n in n_range]
    ax.plot(n_range, o2n2, 'k:', linewidth=2, alpha=0.5, label='O(2ⁿ/²) - Sub-exponential')
    
    # Mark cryptographic security levels
    ax.axvline(x=128, color='purple', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.text(128, 1e-4, '128-bit', rotation=90, fontsize=9, color='purple')
    
    ax.axvline(x=256, color='blue', linestyle=':', alpha=0.5, linewidth=1.5)
    ax.text(256, 1e-4, '256-bit', rotation=90, fontsize=9, color='blue')
    
    ax.set_xlabel('Prime Bit Length (n)', fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
    ax.set_title('Algorithm Complexity Comparison (Random Primes)', fontweight='bold', fontsize=14)
    ax.set_yscale('log')
    ax.set_xlim(15, 60)
    ax.set_ylim(1e-6, 1000)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', ncol=2)
    
    # Add annotation
    ax.text(0.98, 0.02, 'Note: 128-bit would take ~10^25 years\n(impossible for brute force)',
           transform=ax.transAxes, ha='right', va='bottom',
           fontsize=10, style='italic',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    filename = 'graphs/complexity_comparison.png'
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: complexity_comparison.png")

def print_summary():
    """Print data summary"""
    print("\n" + "="*80)
    print("  DATA SUMMARY (Hardcoded from benchmark_results.csv)")
    print("="*80)
    
    print("\nBrute Force (28-bit max due to time constraints):")
    print(f"  Weak primes: {BRUTE_FORCE_DATA.get((28, 'weak'), 0):.2f}s ({BRUTE_FORCE_DATA.get((28, 'weak'), 0)/60:.2f}m)")
    print(f"  Random primes: {BRUTE_FORCE_DATA.get((28, 'random'), 0):.2f}s ({BRUTE_FORCE_DATA.get((28, 'random'), 0)/60:.2f}m)")
    print(f"  Hard primes: {BRUTE_FORCE_DATA.get((28, 'hard'), 0):.2f}s ({BRUTE_FORCE_DATA.get((28, 'hard'), 0)/60:.2f}m)")
    
    print("\nPohlig-Hellman (Vanilla implementation):")
    print(f"  Weak primes: ~0.001s (extremely fast)")
    print(f"  Random primes: ~0.001s")
    print(f"  Hard primes: {POHLIG_HELLMAN_DATA.get((28, 'hard'), 0):.2f}s")
    
    print("\nBSGS (From original benchmark):")
    print(f"  Scales up to 54 bits, max memory ~9GB")
    print(f"  28-bit: ~0.003-0.004s, 54-bit: ~112-234s")
    
    print("\nPollard's Rho (From original benchmark):")
    print(f"  Scales up to 54 bits, constant memory")
    print(f"  28-bit: ~0.006-0.011s, 54-bit: ~237-316s")

def main():
    """Generate all visualizations"""
    print("\n" + "="*80)
    print("  COMPLETE DLP VISUALIZATION")
    print("  Data hardcoded from benchmark_results.csv")
    print("="*80)
    
    print_summary()
    
    # Create graphs directory
    os.makedirs("graphs", exist_ok=True)
    
    print("\nGenerating graphs...\n")
    
    # Individual algorithm plots
    for algo in ALGO_COLORS.keys():
        plot_individual_algorithm(algo, ALL_DATA)
    
    print()
    
    # Dataset comparison plots
    for dataset in ['weak', 'random', 'hard']:
        plot_all_algorithms_comparison(ALL_DATA, dataset)
    
    print()
    
    # Specialized plots
    plot_pohlig_hellman_vulnerability(ALL_DATA)
    plot_brute_force_growth(ALL_DATA)
    plot_performance_summary(ALL_DATA)
    plot_complexity_comparison(ALL_DATA)
    
    print("\n" + "="*80)
    print("  VISUALIZATION COMPLETE")
    print("="*80)
    print("\nGenerated files in ./graphs/ directory:")
    print("  - Individual algorithm performance plots (4)")
    print("  - Dataset comparison plots (3)")
    print("  - Pohlig-Hellman vulnerability plot")
    print("  - Brute force exponential growth plot")
    print("  - 28-bit performance summary")
    print("  - Complexity comparison (with theoretical curves)")
    print("="*80)

if __name__ == "__main__":
    main()