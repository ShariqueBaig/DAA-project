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

def main():
    print("=" * 60)
    print("  DLP Analysis Visualization")
    print("=" * 60)

    rows = load_results()
    if not rows:
        return

    os.makedirs(GRAPH_DIR, exist_ok=True)

    print(f"\n  Generating {len(rows)} test results into visualizations...")
    plot_runtime_vs_bits(rows)
    plot_smooth_vs_nonsmooth(rows)
    plot_memory_analysis(rows)
    plot_algorithm_comparison(rows)

    print(f"\n  All graphs saved to ./{GRAPH_DIR}/")
    print(f"  Generated {len(rows)} result records")

if __name__ == "__main__":
    main()
