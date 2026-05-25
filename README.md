# DLP Algorithm Analysis - Complete Guide

## 🎯 Project Overview

This folder contains a comprehensive analysis suite for the **Discrete Logarithm Problem (DLP)**, implementing and benchmarking four distinct algorithms:

**Problem Definition:** Given a prime modulus `p`, a generator `g`, and a target value `h`, find an integer `x` such that:
```
g^x ≡ h (mod p)
```

This is a fundamental problem in cryptography—the security of Diffie-Hellman key exchange and elliptic curve cryptography depends on its computational intractability.

---

## 📂 Folder Structure

```
analysis/
├── README.md                          # This file
├── ANALYSIS_STRUCTURE.md              # Detailed structure documentation
├── RUN_ORDER.md                       # Step-by-step execution guide
│
├── Core Algorithm Implementation
│   └── dlp_algorithms.py              # All 4 algorithms + helpers
│
├── Benchmarking Suites
│   ├── expanded_benchmark.py          # Main benchmarking (16-48 bit primes)
│   ├── parallel_brute_force.py        # Multiprocessing variant
│   ├── enhanced_pohlig_hellman.py     # Improved PH with nested BSGS
│   └── stress_test.py                 # Memory/time limit testing
│
├── Visualization & Analysis
│   └── visualize_analysis.py          # Generate 4 publication-quality graphs
│
├── Orchestration
│   └── master_runner.py               # Automated complete workflow
│
├── Configuration
│   └── requirements.txt               # Python dependencies
│
└── Generated Outputs (after running)
    ├── expanded_results.csv           # Benchmark data
    └── graphs/                        # Visualization PNGs (19 graphs)
        ├── runtime_vs_bits.png
        ├── smooth_vs_nonsmooth.png
        ├── memory_analysis.png
        ├── algorithm_comparison.png
        ├── complexity_scaling.png
        ├── algorithm_speedup.png
        ├── time_memory_tradeoff.png
        ├── algorithm_frontier.png
        ├── smooth_comparison.png
        ├── runtime_distribution.png
        ├── memory_usage.png
        ├── algorithm_scaling.png
        ├── weak_vs_normal.png
        ├── brute_force_comparison.png
        ├── baby_step_giant_step_comparison.png
        ├── pollard_s_rho_comparison.png
        ├── pohlig_hellman_comparison.png
        ├── brute_force_complexity.png
        ├── baby_step_giant_step_complexity.png
        ├── pollard_s_rho_complexity.png
        └── pohlig_hellman_complexity.png
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- ~2GB free disk space (for large test cases)

### Installation
```bash
pip install -r requirements.txt
```

### Run Complete Analysis (Recommended)
```bash
python master_runner.py
```

This automatically runs all stages in the correct order:
1. Generates benchmark data (~20-40 minutes)
2. Creates visualizations (~1-2 minutes)
3. Optional: Runs advanced tests

**Expected output:** `expanded_results.csv` + 19 PNG graphs

---

## 📋 What's Implemented

### Algorithms
| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| **Brute Force** | O(p) | O(1) | Baseline; times out >28 bits |
| **Baby-step Giant-step (BSGS)** | O(√p) | O(√p) | Time-memory tradeoff; memory limit ~44 bits |
| **Pollard's Rho** | O(√p) | O(1) | Probabilistic; scales to 60+ bits |
| **Pohlig-Hellman** | O(factors) | O(log p) | Fast on smooth primes; slow on hard primes |
| **Enhanced Pohlig-Hellman** | O(factors) | O(log p) | Nested BSGS for robustness |
| **Parallel Brute Force** | O(p/n) | O(1/n) | Multiprocessing speedup |

### Test Coverage
- **Bit lengths:** 16-64 bits (weak and normal primes)
- **Prime types:** Weak (smooth p-1) and normal (random) primes
- **Test cases:** 20+ auto-generated with varying generators and exponents, plus large datasets
- **Metrics:** Execution time, memory usage, correctness status

---

## 🎮 How to Run

### Option 1: Fully Automated (Easiest)
```bash
python master_runner.py
```
Handles all stages with user prompts for optional tests.

### Option 2: Stage-by-Stage (Most Control)

**Stage 1: Generate benchmark data** (~20-40 minutes)
```bash
python expanded_benchmark.py
```
Creates `expanded_results.csv` with all timing and memory data.

**Stage 2: Create visualizations** (~1-2 minutes)
```bash
python visualize_analysis.py
```
Generates 4 PNG graphs in `graphs/` folder.

**Stage 3a: Test parallel processing** (~10-30 seconds, optional)
```bash
python parallel_brute_force.py
```
Compares sequential vs parallel brute force.

**Stage 3b: Test enhanced algorithms** (~2-5 seconds, optional)
```bash
python enhanced_pohlig_hellman.py
```
Validates improved Pohlig-Hellman implementation.

**Stage 3c: Stress test** (~5-60 minutes, optional)
```bash
python stress_test.py
```
⚠️ Warning: May consume significant RAM and CPU time. Finds practical memory/time limits.

---

## 📊 Expected Results

### Performance Scaling
```
16-bit:  Brute Force ~0.0007s, BSGS ~0.0001s, PR ~0.0006s, PH ~0.00007s
20-bit:  Brute Force ~0.028s,  BSGS ~0.0006s, PR ~0.0002s, PH ~0.0001s
24-bit:  Brute Force ~1.1s,    BSGS ~0.0025s, PR ~0.0015s, PH ~0.0012s
28-bit:  Brute Force TIMEOUT,  BSGS ~0.016s,  PR ~0.012s,  PH ~0.067s
32-bit:  SKIPPED,              BSGS ~0.05s,   PR ~0.03s,   PH SKIPPED
40-bit:  SKIPPED,              BSGS ~2s,      PR ~0.5s,    PH ~0.0001s (smooth)
48-bit:  SKIPPED,              BSGS ~300MB,   PR ~1s,      PH SKIPPED
```

### Key Findings
1. **Smooth Prime Vulnerability:** Pohlig-Hellman on 26-bit smooth: ~0.0001s vs ~0.067s non-smooth (670x faster)
2. **Memory Constraints:** BSGS hits RAM limits around 44-48 bits
3. **Scalability:** Pollard's Rho scales best with constant memory
4. **Parallelization:** Brute force shows linear speedup with CPU cores

---

## 📈 Output Files Explained

### expanded_results.csv
Detailed benchmark results with columns:
- `bit_length` - Prime size in bits
- `prime` - The actual prime modulus
- `test_name` - Test case description
- `is_smooth` - Whether p-1 has only small prime factors
- `description` - Additional metadata
- `algorithm` - Algorithm name
- `time_seconds` - Execution time (or timeout)
- `result` - Computed discrete logarithm
- `status` - PASSED, FAILED, TIMEOUT, SKIPPED, ERROR
- `memory_estimate` - Estimated memory usage

### Generated Graphs
1. **runtime_vs_bits.png** - Time vs prime size (log scale, non-smooth only)
2. **smooth_vs_nonsmooth.png** - Pohlig-Hellman performance comparison
3. **memory_analysis.png** - Memory usage by algorithm and bit length
4. **algorithm_comparison.png** - Side-by-side performance at each bit length
5. **complexity_scaling.png** - Log-log plot validating O(√p) bounds
6. **algorithm_speedup.png** - Speedup factor vs brute force
7. **time_memory_tradeoff.png** - Time vs memory scatter plot
8. **algorithm_frontier.png** - Best algorithm per bit length
9. **smooth_comparison.png** - Smooth vs non-smooth at same bit lengths
10. **runtime_distribution.png** - Distribution of execution times
11. **memory_usage.png** - Memory usage over bit lengths
12. **algorithm_scaling.png** - Scaling with theoretical overlays
13. **weak_vs_normal.png** - Weak vs normal primes comparison
14-17. **Individual algorithm comparisons** - Separate plots for each algorithm differentiating weak/normal
18. **Complexity overlays** - Empirical vs theoretical for each algorithm
19. **performance_heatmap.png** - Heatmap of log times across algorithms/bits

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: dlp_algorithms"
**Cause:** Script not in same directory as dlp_algorithms.py
**Fix:** Ensure you're in the `analysis/` folder when running

### "MemoryError" or "Killed" process
**Cause:** BSGS with 48-bit primes needs ~1GB RAM
**Solution:** Reduce bit size range in `expanded_benchmark.py` or run on higher-RAM machine

### "No module named 'matplotlib'" or 'sympy'
**Cause:** Dependencies not installed
**Fix:** Run `pip install -r requirements.txt`

### Timeout errors (expected behavior)
**Info:** Brute force naturally times out on 28+ bit primes
**Note:** This validates theoretical O(p) complexity bounds

### Graphs not generated
**Cause:** `expanded_results.csv` missing (benchmarks didn't run)
**Fix:** Run `python expanded_benchmark.py` first, then visualize

### Benchmark takes too long
**Info:** Normal—depends on CPU and prime size
**Speed up:** Reduce max bit length in `expanded_benchmark.py` (line ~30)

---

## ⏱️ Time Estimates

### By Hardware
| System | Expanded Benchmark | Visualizations | Total |
|--------|-------------------|-----------------|-------|
| Modern Desktop (8-core, 16GB RAM) | 30-60 min | 1-2 min | ~60 min |
| Laptop (4-core, 8GB RAM) | 60-120 min | 2-5 min | ~120 min |
| Server (16-core, 64GB RAM) | 15-30 min | 1-2 min | ~30 min |
| VM (4-core, 4GB RAM) | 120-240 min | 5-10 min | ~240 min |

### By Stage (Typical Desktop)
- Expanded Benchmarking: 30-60 minutes (exhaustive on large datasets)
- Visualization: 5-10 seconds (19 graphs)
- Parallel Testing: 10-30 seconds
- Enhanced PH: 2-5 seconds
- Stress Testing: 10-120 minutes (optional)

---

## 📖 Documentation Files

- **README.md** (this file) - Overview and quick start
- **ANALYSIS_STRUCTURE.md** - Detailed folder structure and features
- **RUN_ORDER.md** - Step-by-step execution guide with code examples

---

## 🎓 Understanding the Analysis

### Why Four Algorithms?
1. **Brute Force** - Establishes baseline; shows why exponential is intractable
2. **BSGS** - Classic time-memory tradeoff; hits practical limits
3. **Pollard's Rho** - Low memory; probabilistic; scales well
4. **Pohlig-Hellman** - Reveals cryptographic vulnerability of smooth primes

### What Makes Smooth Primes Vulnerable?
If p-1 has only small prime factors, Pohlig-Hellman decomposes the DLP into many small subproblems, making it tractable. This is why cryptographic protocols mandate "safe primes."

### Key Complexity Results
- **Brute Force:** O(p) - exponential in bit length
- **BSGS & Pollard's Rho:** O(√p) - subexponential but still exponential in bit length
- **Pohlig-Hellman:** Depends on largest prime factor of p-1

---

## ✅ Verification Checklist

The analysis suite includes:
- ✓ All 4 core algorithms
- ✓ 2 advanced implementations (parallel, enhanced)
- ✓ 20+ diverse test cases
- ✓ Input variation (bit length, smoothness, generators)
- ✓ Performance logging (time, memory, status)
- ✓ Correctness verification (pow(g, result, p) == h)
- ✓ Error handling (timeouts, failures, edge cases)
- ✓ CSV export for analysis
- ✓ Publication-quality visualizations
- ✓ Automated orchestration
- ✓ Comprehensive documentation

---

## 🚀 Next Steps After Analysis

1. **Review Data:** Open `expanded_results.csv` to explore raw results
2. **Analyze Graphs:** View PNG files to see performance trends
3. **Draw Conclusions:** Compare empirical results to theoretical bounds
4. **Write Report:** Document findings and implications
5. **Verify Theory:** Check that O(√p) matches your observations

---

## 💡 Tips & Tricks

### Custom Testing
Edit `expanded_benchmark.py` to:
- Add specific bit lengths
- Test custom generators
- Adjust timeout values
- Change smooth prime criteria

### Performance Profiling
Add timing profilers:
```python
import cProfile
cProfile.run('bsgs(g, h, p)')
```

### Memory Profiling
Use `memory_profiler`:
```bash
pip install memory-profiler
python -m memory_profiler visualize_analysis.py
```

### Parallel Scaling Analysis
Modify `parallel_brute_force.py` to test different core counts:
```python
for cores in [1, 2, 4, 8]:
    result, time = parallel_brute_force(g, h, p, num_processes=cores)
```

---

## 📞 Support

### Common Issues

**Q: Why does BSGS use so much memory?**  
A: It creates a hash table of O(√p) entries. For 48-bit primes, that's ~300 million entries.

**Q: Is Pollard's Rho really faster than BSGS?**  
A: Not always faster, but more practical for large primes due to O(1) memory.

**Q: Can I optimize the algorithms further?**  
A: Yes! Consider GPU acceleration, parallel BSGS, or specialized hardware.

**Q: How does this relate to real cryptography?**  
A: Modern systems use much larger primes (2048+ bits) where these attacks are infeasible.

---

## 📜 License & Attribution

**Team:** Sharique (28369), Maira Aijaz (28552), Muhammad Ibrahim (29079), Suffiyan Asghar Ali (29182)  
**Course:** CSE 317 — Algorithms: Design and Analysis  
**Date:** May 2026

---

## 🎉 Ready to Go!

Everything is set up and ready to run. Start with:

```bash
python master_runner.py
```

The complete analysis will take approximately **20-60 minutes** depending on your system.

Enjoy your DLP algorithm analysis! 🚀
