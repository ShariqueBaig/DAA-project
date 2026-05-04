# Analysis Folder - Complete Run Order

## Overview
This folder contains the complete DLP algorithm analysis suite. All scripts are self-contained and organized for sequential execution.

## Prerequisites
Install dependencies:
```bash
pip install -r requirements.txt
```

## Recommended Execution Order

### Stage 1: Core Benchmarking
Run the standard benchmark suite with diverse test cases:

```bash
python expanded_benchmark.py
```

**Output:**
- `expanded_results.csv` - detailed benchmark data with memory estimates
- Console output with all test case results

**Duration:** ~5-30 minutes depending on CPU and system load

**What it does:**
- Tests 16-bit to 48-bit primes
- Includes both smooth and random primes
- Generates smooth primes dynamically
- Logs performance metrics for each algorithm
- Estimates memory usage

---

### Stage 2: Visualization Generation
Generate publication-quality graphs from benchmark data:

```bash
python visualize_analysis.py
```

**Output:**
- `graphs/runtime_vs_bits.png` - Time vs prime size (log scale)
- `graphs/smooth_vs_nonsmooth.png` - Pohlig-Hellman vulnerability
- `graphs/memory_analysis.png` - Memory usage estimates
- `graphs/algorithm_comparison.png` - Side-by-side performance

**Duration:** ~2-5 seconds

**Note:** Requires `expanded_results.csv` from Stage 1

---

### Stage 3: Advanced Testing (Optional)

#### 3a. Parallel Processing Validation
Test parallel brute force implementation:

```bash
python parallel_brute_force.py
```

**Output:** Performance comparison between sequential and parallel implementations

**Duration:** ~10-30 seconds

---

#### 3b. Enhanced Pohlig-Hellman
Test improved PH with nested BSGS:

```bash
python enhanced_pohlig_hellman.py
```

**Output:** Results from enhanced algorithm on sample cases

**Duration:** ~2-5 seconds

---

#### 3c. Stress Testing
Find practical limits and memory boundaries:

```bash
python stress_test.py
```

**Output:** Runtime and memory usage at various input sizes

**Duration:** ~5-60 minutes (depending on hardware)

**Warning:** May consume significant RAM on large inputs

---

## Complete Workflow (Fastest Path)

For a complete analysis in minimum time:

```bash
# 1. Generate all data (required)
python expanded_benchmark.py

# 2. Generate visualizations (required)
python visualize_analysis.py

# 3. Optional: Verify implementations
python parallel_brute_force.py
python enhanced_pohlig_hellman.py
```

**Total time: ~30-60 minutes**

---

## File Descriptions

### Input Files
- `dlp_algorithms.py` - Core algorithm implementations
- `requirements.txt` - Python dependencies

### Benchmark Scripts
- `expanded_benchmark.py` - Main benchmarking suite with diverse test cases
- `parallel_brute_force.py` - Multiprocessing parallelization test
- `enhanced_pohlig_hellman.py` - Improved PH algorithm test
- `stress_test.py` - Memory and timeout limit testing

### Analysis Scripts
- `visualize_analysis.py` - Graph generation from benchmark results

### Output Files
- `expanded_results.csv` - Benchmark results (generated)
- `graphs/` - PNG visualizations (generated)

---

## Data Interpretation

### expanded_results.csv Columns
| Column | Description |
|--------|-------------|
| bit_length | Prime size in bits |
| prime | The actual prime modulus used |
| test_name | Descriptive name of test case |
| is_smooth | Whether p-1 has only small factors |
| description | Additional test metadata |
| algorithm | Algorithm name (4 variants) |
| time_seconds | Execution time in seconds |
| result | Computed discrete logarithm |
| status | PASSED, FAILED, TIMEOUT, SKIPPED, ERROR |
| memory_estimate | Estimated memory usage in bytes |

---

## Expected Results Summary

### Performance Scaling
- **Brute Force:** O(p) - exponential growth, times out ~28-30 bits
- **BSGS:** O(√p) - square root scaling, memory limits ~40-44 bits
- **Pollard's Rho:** O(√p) - square root with constant memory
- **Pohlig-Hellman:** Depends on prime factorization - fastest on smooth primes

### Smooth Prime Advantage
- Pohlig-Hellman on 26-bit smooth prime: ~0.0001s
- Pohlig-Hellman on 26-bit non-smooth prime: ~0.067s
- **Speedup: 670x faster on smooth primes**

### Memory Usage
- Brute Force: ~1 KB
- Pollard's Rho: ~1 KB
- BSGS: O(√p) - ~1 MB for 32-bit, ~300 MB for 48-bit
- Pohlig-Hellman: ~100 KB

---

## Troubleshooting

### ModuleNotFoundError: dlp_algorithms
**Solution:** Ensure `dlp_algorithms.py` is in the same folder

### MemoryError during BSGS
**Cause:** BSGS with 48-bit primes needs ~1 GB RAM
**Solution:** Skip or reduce test size in expanded_benchmark.py

### Timeout errors
**Expected:** Brute force naturally times out on large inputs (28+ bits)
**Note:** This validates theoretical bounds

### Missing graphs
**Solution:** Run `expanded_benchmark.py` first to generate CSV data

---

## Next Steps

1. **Review Results:** Examine `expanded_results.csv` for performance data
2. **Analyze Graphs:** View PNG files in `graphs/` folder
3. **Compare Findings:** Cross-reference with project documentation
4. **Draw Conclusions:** Verify theoretical complexity bounds empirically

---

## Time Estimates by System

| Hardware | Expanded Benchmark | Visualizations | Total |
|----------|-------------------|-----------------|-------|
| Modern Desktop (8-core) | 10-20 min | <1 min | ~20 min |
| Laptop (4-core) | 20-40 min | 1-2 min | ~40 min |
| High-end Workstation | 5-10 min | <1 min | ~10 min |
| Virtual Machine | 30-60 min | 2-5 min | ~60 min |

---

## Output Organization

After running, your `analysis/` folder will contain:

```
analysis/
├── dlp_algorithms.py                    (core - input)
├── expanded_benchmark.py                (runner - input)
├── parallel_brute_force.py              (optional - input)
├── enhanced_pohlig_hellman.py           (optional - input)
├── stress_test.py                       (optional - input)
├── visualize_analysis.py                (runner - input)
├── requirements.txt                     (dependencies)
├── RUN_ORDER.md                         (this file)
├── expanded_results.csv                 (output - data)
└── graphs/                              (output - visualizations)
    ├── runtime_vs_bits.png
    ├── smooth_vs_nonsmooth.png
    ├── memory_analysis.png
    └── algorithm_comparison.png
```
