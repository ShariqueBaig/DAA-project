"""
DLP Analysis Visualization
Reads expanded_results.csv and generates publication-quality graphs.
Usage: python visualize_analysis.py
"""
import csv, os, math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving PNGs

GRAPH_DIR = "graphs"
CSV_FILE = "expanded_results.csv"

# Color palette - professional and distinct
COLORS = {
    "Brute Force":          "#e74c3c",
    "Baby-step Giant-step": "#3498db",
    "Pollard's Rho":        "#2ecc71",
    "Pohlig-Hellman":       "#f39c12",
}
MARKERS = {
    "Brute Force":          "o",
    "Baby-step Giant-step": "s",
    "Pollard's Rho":        "D",
    "Pohlig-Hellman":       "^",
}

def load_results():
    rows = []
    if not os.path.exists(CSV_FILE):
        print(f"ERROR: {CSV_FILE} not found. Run expanded_benchmark.py first.")
        return []
    
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["bit_length"] = int(row["bit_length"])
            row["is_smooth"] = row["is_smooth"] == "True"
            if row["time_seconds"] and row["time_seconds"] != "None":
                try:
                    row["time_seconds"] = float(row["time_seconds"])
                except:
                    row["time_seconds"] = None
            else:
                row["time_seconds"] = None
            rows.append(row)
    return rows

def setup_style():
    plt.rcParams.update({
        'figure.facecolor': '#1a1a2e',
        'axes.facecolor': '#16213e',
        'axes.edgecolor': '#e0e0e0',
        'axes.labelcolor': '#e0e0e0',
        'text.color': '#e0e0e0',
        'xtick.color': '#e0e0e0',
        'ytick.color': '#e0e0e0',
        'grid.color': '#2a2a4a',
        'grid.alpha': 0.6,
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'legend.fontsize': 11,
        'figure.titlesize': 18,
    })

def plot_runtime_vs_bits(rows):
    """Graph 1: Runtime vs Bit Length (log scale) - all algorithms."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    algo_data = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED":
            continue
        if r["is_smooth"]:
            continue
        algo = r["algorithm"]
        if algo not in algo_data:
            algo_data[algo] = {"bits": [], "times": []}
        algo_data[algo]["bits"].append(r["bit_length"])
        algo_data[algo]["times"].append(r["time_seconds"])

    for algo, data in algo_data.items():
        sorted_pairs = sorted(zip(data["bits"], data["times"]))
        bits, times = zip(*sorted_pairs) if sorted_pairs else ([], [])
        ax.plot(bits, times,
                marker=MARKERS.get(algo, "o"), color=COLORS.get(algo, "#fff"),
                linewidth=2.5, markersize=9, label=algo, alpha=0.9)

    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_title("DLP Algorithm Runtime vs. Prime Size", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "runtime_vs_bits.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_smooth_vs_nonsmooth(rows):
    """Graph 2: Performance on smooth vs non-smooth primes."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    smooth = {"bits": [], "times": []}
    nonsmooth = {"bits": [], "times": []}

    for r in rows:
        if r["algorithm"] != "Pohlig-Hellman":
            continue
        if r["time_seconds"] is None or r["status"] != "PASSED":
            continue
        if r["is_smooth"]:
            smooth["bits"].append(r["bit_length"])
            smooth["times"].append(r["time_seconds"])
        else:
            nonsmooth["bits"].append(r["bit_length"])
            nonsmooth["times"].append(r["time_seconds"])

    if smooth["bits"]:
        sorted_smooth = sorted(zip(smooth["bits"], smooth["times"]))
        sbits, stimes = zip(*sorted_smooth)
        ax.plot(sbits, stimes,
                marker="^", color="#2ecc71", linewidth=2.5, markersize=10,
                label="Pohlig-Hellman (smooth p-1)", alpha=0.9)
    if nonsmooth["bits"]:
        sorted_nonsmooth = sorted(zip(nonsmooth["bits"], nonsmooth["times"]))
        nbits, ntimes = zip(*sorted_nonsmooth)
        ax.plot(nbits, ntimes,
                marker="v", color="#e74c3c", linewidth=2.5, markersize=10,
                label="Pohlig-Hellman (non-smooth p-1)", alpha=0.9)

    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_title("Pohlig-Hellman: Impact of Prime Structure",
                 fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "smooth_vs_nonsmooth.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_memory_analysis(rows):
    """Graph 3: Memory usage estimation by algorithm."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    algo_mem = {}
    for r in rows:
        if r["memory_estimate"] is None or r["status"] != "PASSED":
            continue
        algo = r["algorithm"]
        if algo not in algo_mem:
            algo_mem[algo] = {"bits": [], "mem": []}
        algo_mem[algo]["bits"].append(r["bit_length"])
        algo_mem[algo]["mem"].append(float(r["memory_estimate"]))

    for algo, data in algo_mem.items():
        sorted_pairs = sorted(zip(data["bits"], data["mem"]))
        bits, mem = zip(*sorted_pairs) if sorted_pairs else ([], [])
        ax.plot(bits, mem,
                marker=MARKERS.get(algo, "o"), color=COLORS.get(algo, "#fff"),
                linewidth=2.5, markersize=9, label=algo, alpha=0.9)

    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Memory (bytes, log scale)")
    ax.set_title("Memory Usage Estimation by Algorithm", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "memory_analysis.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_algorithm_comparison(rows):
    """Graph 4: Algorithm comparison at similar bit lengths."""
    setup_style()
    fig, ax = plt.subplots(figsize=(14, 7))

    data = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED":
            continue
        if r["is_smooth"]:
            continue
        bl = r["bit_length"]
        if bl not in data:
            data[bl] = {}
        data[bl][r["algorithm"]] = r["time_seconds"]

    bit_lengths = sorted(data.keys())
    algos = ["Brute Force", "Baby-step Giant-step", "Pollard's Rho", "Pohlig-Hellman"]
    x_pos = range(len(bit_lengths))
    bar_width = 0.18

    for i, algo in enumerate(algos):
        vals = [data[bl].get(algo, 0) for bl in bit_lengths]
        offset = (i - 1.5) * bar_width
        ax.bar([x + offset for x in x_pos], vals, bar_width,
                label=algo, color=COLORS.get(algo, "#fff"), alpha=0.85, edgecolor="#222")

    ax.set_xticks(list(x_pos))
    ax.set_xticklabels([f"{bl}-bit" for bl in bit_lengths])
    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_title("Algorithm Comparison (Non-Smooth Primes)", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "algorithm_comparison.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_complexity_scaling(rows):
    """Graph 5: Log-log plot to validate O(sqrt(p)) vs O(p) theoretical bounds."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    algo_data = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED":
            continue
        if r["is_smooth"]:
            continue
        algo = r["algorithm"]
        if algo not in algo_data:
            algo_data[algo] = {"bits": [], "times": []}
        algo_data[algo]["bits"].append(r["bit_length"])
        algo_data[algo]["times"].append(r["time_seconds"])

    # Plot empirical on log-log
    for algo, data in algo_data.items():
        sorted_pairs = sorted(zip(data["bits"], data["times"]))
        bits, times = zip(*sorted_pairs) if sorted_pairs else ([], [])
        ax.loglog(bits, times,
                marker=MARKERS.get(algo, "o"), color=COLORS.get(algo, "#fff"),
                linewidth=2.5, markersize=9, label=algo, alpha=0.9)

    # Add theoretical lines (normalized)
    if len(algo_data) > 0:
        bit_range = [16, 20, 24, 28, 32, 40]
        # O(2^n) reference (exponential)
        exp_times = [2**(n/8) * 0.001 for n in bit_range]
        ax.loglog(bit_range, exp_times, '--', color='#e74c3c', alpha=0.3, linewidth=2, label='O(2^n) reference')
        
        # O(2^(n/2)) reference (sqrt)
        sqrt_times = [2**(n/16) * 0.001 for n in bit_range]
        ax.loglog(bit_range, sqrt_times, '--', color='#3498db', alpha=0.3, linewidth=2, label='O(2^(n/2)) reference')

    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title("Complexity Scaling Validation (Log-Log)", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4, which="both")
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "complexity_scaling.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_algorithm_speedup(rows):
    """Graph 6: Speedup factor (how much faster each is vs Brute Force)."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    # Collect BF baseline for each bit length
    bf_times = {}
    for r in rows:
        if r["algorithm"] == "Brute Force" and r["time_seconds"] and r["status"] == "PASSED":
            bf_times[r["bit_length"]] = r["time_seconds"]

    # Calculate speedups
    algo_speedups = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED" or r["algorithm"] == "Brute Force":
            continue
        if r["is_smooth"]:
            continue
        bl = r["bit_length"]
        if bl in bf_times:
            speedup = bf_times[bl] / r["time_seconds"]
            if r["algorithm"] not in algo_speedups:
                algo_speedups[r["algorithm"]] = {"bits": [], "speedup": []}
            algo_speedups[r["algorithm"]]["bits"].append(bl)
            algo_speedups[r["algorithm"]]["speedup"].append(speedup)

    for algo, data in algo_speedups.items():
        sorted_pairs = sorted(zip(data["bits"], data["speedup"]))
        bits, speedups = zip(*sorted_pairs) if sorted_pairs else ([], [])
        ax.plot(bits, speedups,
                marker=MARKERS.get(algo, "o"), color=COLORS.get(algo, "#fff"),
                linewidth=2.5, markersize=9, label=algo, alpha=0.9)

    ax.axhline(y=1, color='#e74c3c', linestyle=':', linewidth=2, alpha=0.5, label='Brute Force baseline')
    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Speedup Factor (relative to Brute Force)")
    ax.set_title("Algorithm Speedup vs Brute Force", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "algorithm_speedup.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_time_memory_tradeoff(rows):
    """Graph 7: Time vs Memory tradeoff visualization."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    # Collect time and memory for each algorithm at each size
    algo_tradeoff = {}
    for r in rows:
        if r["time_seconds"] is None or r["memory_estimate"] is None or r["status"] != "PASSED":
            continue
        if r["is_smooth"]:
            continue
        algo = r["algorithm"]
        if algo not in algo_tradeoff:
            algo_tradeoff[algo] = {"time": [], "mem": [], "bits": []}
        algo_tradeoff[algo]["time"].append(r["time_seconds"])
        algo_tradeoff[algo]["mem"].append(float(r["memory_estimate"]))
        algo_tradeoff[algo]["bits"].append(r["bit_length"])

    for algo, data in algo_tradeoff.items():
        scatter = ax.scatter(data["mem"], data["time"], 
                           s=200, alpha=0.7, color=COLORS.get(algo, "#fff"),
                           marker=MARKERS.get(algo, "o"), label=algo, edgecolors='white', linewidth=2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Memory Usage (bytes, log scale)")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_title("Time-Memory Tradeoff Analysis", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4, which="both")
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "time_memory_tradeoff.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_algorithm_frontier(rows):
    """Graph 8: Algorithm scalability frontier - best algorithm for each bit length."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    # Find fastest algorithm at each bit length
    best_algo = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED" or r["is_smooth"]:
            continue
        bl = r["bit_length"]
        if bl not in best_algo or r["time_seconds"] < best_algo[bl]["time"]:
            best_algo[bl] = {"algo": r["algorithm"], "time": r["time_seconds"]}

    # Group by algorithm
    algo_frontier = {}
    for bl, data in sorted(best_algo.items()):
        algo = data["algo"]
        if algo not in algo_frontier:
            algo_frontier[algo] = {"bits": [], "times": []}
        algo_frontier[algo]["bits"].append(bl)
        algo_frontier[algo]["times"].append(data["time"])

    # Plot stacked area to show transition
    for algo, data in algo_frontier.items():
        ax.plot(data["bits"], data["times"],
                marker=MARKERS.get(algo, "o"), color=COLORS.get(algo, "#fff"),
                linewidth=3, markersize=10, label=f'{algo} (optimal)', alpha=0.9)

    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Optimal Time (seconds, log scale)")
    ax.set_title("Algorithm Scalability Frontier - Best Performance Per Size", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "algorithm_frontier.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_smooth_prime_comparison(rows):
    """Graph 9: Direct comparison of same bit-length on smooth vs non-smooth."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    # Find pairs of same bit-length, different smoothness
    comparisons = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED":
            continue
        key = (r["bit_length"], r["algorithm"])
        if key not in comparisons:
            comparisons[key] = []
        comparisons[key].append({"smooth": r["is_smooth"], "time": r["time_seconds"]})

    # Plot comparison bars for each algorithm
    algos = ["Baby-step Giant-step", "Pollard's Rho", "Pohlig-Hellman"]
    bit_lengths = sorted(set(bl for bl, algo in comparisons.keys()))
    x_pos = range(len(bit_lengths))
    bar_width = 0.25

    for i, algo in enumerate(algos):
        smooth_times = []
        nonsmooth_times = []
        for bl in bit_lengths:
            key = (bl, algo)
            if key in comparisons:
                smooth = [d["time"] for d in comparisons[key] if d["smooth"]]
                nonsmooth = [d["time"] for d in comparisons[key] if not d["smooth"]]
                smooth_times.append(smooth[0] if smooth else 0)
                nonsmooth_times.append(nonsmooth[0] if nonsmooth else 0)
            else:
                smooth_times.append(0)
                nonsmooth_times.append(0)

        offset = (i - 1) * bar_width
        if any(t > 0 for t in smooth_times):
            ax.bar([x + offset - bar_width/2 for x in x_pos], smooth_times, bar_width,
                    label=f'{algo} (smooth)', color=COLORS.get(algo, "#fff"), alpha=0.8, edgecolor="#222")
        if any(t > 0 for t in nonsmooth_times):
            ax.bar([x + offset + bar_width/2 for x in x_pos], nonsmooth_times, bar_width,
                    label=f'{algo} (non-smooth)', color=COLORS.get(algo, "#fff"), alpha=0.4, edgecolor="#222")

    ax.set_xticks(list(x_pos))
    ax.set_xticklabels([f"{bl}-bit" for bl in bit_lengths])
    ax.set_yscale("log")
    ax.set_xlabel("Prime Bit Length")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_title("Smooth vs Non-Smooth Prime Impact (Same Bit Length)", fontweight="bold", pad=15)
    ax.legend(loc="upper left", framealpha=0.8, facecolor="#16213e", edgecolor="#444", fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "smooth_comparison.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def plot_consistency_distribution(rows):
    """Graph 10: Distribution of times across multiple runs (if available)."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 7))

    # Group times by algorithm and bit length
    time_dist = {}
    for r in rows:
        if r["time_seconds"] is None or r["status"] != "PASSED" or r["is_smooth"]:
            continue
        key = (r["bit_length"], r["algorithm"])
        if key not in time_dist:
            time_dist[key] = []
        time_dist[key].append(r["time_seconds"])

    # Box plot data
    labels = []
    data = []
    colors_list = []
    bit_lengths = sorted(set(bl for bl, _ in time_dist.keys()))
    
    for bl in bit_lengths:
        for algo in ["Brute Force", "Baby-step Giant-step", "Pollard's Rho", "Pohlig-Hellman"]:
            key = (bl, algo)
            if key in time_dist and len(time_dist[key]) > 0:
                labels.append(f"{bl}b-{algo[:2]}")
                data.append(time_dist[key])
                colors_list.append(COLORS.get(algo, "#fff"))

    if data:
        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

    ax.set_yscale("log")
    ax.set_ylabel("Execution Time (seconds, log scale)")
    ax.set_xlabel("Bit Length - Algorithm")
    ax.set_title("Runtime Distribution by Algorithm and Size", fontweight="bold", pad=15)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, "runtime_distribution.png")
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved: {path}")

def main():
    print("=" * 60)
    print("  DLP Analysis Visualization")
    print("=" * 60)

    rows = load_results()
    if not rows:
        return

    os.makedirs(GRAPH_DIR, exist_ok=True)

    print(f"\n  Generating {len(rows)} test results into visualizations...")
    print("  [1/10] Runtime vs Bit Length...")
    plot_runtime_vs_bits(rows)
    print("  [2/10] Smooth vs Non-smooth...")
    plot_smooth_vs_nonsmooth(rows)
    print("  [3/10] Memory Analysis...")
    plot_memory_analysis(rows)
    print("  [4/10] Algorithm Comparison...")
    plot_algorithm_comparison(rows)
    print("  [5/10] Complexity Scaling...")
    plot_complexity_scaling(rows)
    print("  [6/10] Algorithm Speedup...")
    plot_algorithm_speedup(rows)
    print("  [7/10] Time-Memory Tradeoff...")
    plot_time_memory_tradeoff(rows)
    print("  [8/10] Algorithm Frontier...")
    plot_algorithm_frontier(rows)
    print("  [9/10] Smooth Comparison...")
    plot_smooth_prime_comparison(rows)
    print("  [10/10] Runtime Distribution...")
    plot_consistency_distribution(rows)

    print(f"\n  ✓ All 10 graphs saved to ./{GRAPH_DIR}/")
    print(f"  ✓ Generated {len(rows)} result records")

if __name__ == "__main__":
    main()
