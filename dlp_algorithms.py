import math
import time
import random

# 1. Naive Brute Force (with optional timeout)
def brute_force(g, h, p, timeout=60):
    start = time.perf_counter()
    for x in range(p):
        if pow(g, x, p) == h:
            return x
        # Check timeout every 10,000 iterations to avoid overhead
        if x % 10000 == 0 and time.perf_counter() - start > timeout:
            return "TIMEOUT"
    return None

# --- Helper Math Functions ---
def ext_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modInverse(a, m):
    gcd, x, y = ext_gcd(a, m)
    if gcd != 1:
        return None
    return x % m

# 2. Baby-step Giant-step
def bsgs(g, h, p):
    m = math.ceil(math.sqrt(p))
    table = {}
    
    # Baby steps
    for j in range(m):
        table[pow(g, j, p)] = j
    
    # Giant steps
    gm = pow(g, m, p)
    c = modInverse(gm, p)
    if c is None: return None
        
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * c) % p
    return None

# 3. Pollard's Rho (with retry mechanism)
def _pollards_rho_once(g, h, p):
    """Single attempt of Pollard's Rho. May return None on unlucky random start."""
    N = p - 1
    def new_xab(x, a, b):
        partition = x % 3
        if partition == 0:
            return (x * x) % p, (a * 2) % N, (b * 2) % N
        elif partition == 1:
            return (x * g) % p, (a + 1) % N, b
        else:
            return (x * h) % p, a, (b + 1) % N

    # Randomize start to prevent trivial immediate loops
    a_i, b_i = random.randint(1, N-1), random.randint(1, N-1)
    x_i = (pow(g, a_i, p) * pow(h, b_i, p)) % p
    x_2i, a_2i, b_2i = x_i, a_i, b_i
    
    for _ in range(N):
        x_i, a_i, b_i = new_xab(x_i, a_i, b_i)
        x_2i, a_2i, b_2i = new_xab(x_2i, a_2i, b_2i)
        x_2i, a_2i, b_2i = new_xab(x_2i, a_2i, b_2i)
        
        if x_i == x_2i:
            break
            
    r = (b_i - b_2i) % N
    if r == 0: return None
    
    target = (a_2i - a_i) % N
    gcd, inv_r, _ = ext_gcd(r, N)
    
    if target % gcd != 0: return None
        
    res = (inv_r * (target // gcd)) % (N // gcd)
    
    for k in range(gcd):
        check = (res + k * (N // gcd)) % N
        if pow(g, check, p) == h:
            return check
    return None

def pollards_rho(g, h, p, max_attempts=20):
    """Robust Pollard's Rho with automatic retry on failure."""
    for attempt in range(max_attempts):
        result = _pollards_rho_once(g, h, p)
        if result is not None:
            return result
    return None

# --- Helpers for Pohlig-Hellman ---
def crt(remainders, moduli):
    sum_val = 0
    prod = 1
    for m in moduli: prod *= m
    for r, m in zip(remainders, moduli):
        p_i = prod // m
        sum_val += r * modInverse(p_i, m) * p_i
    return sum_val % prod

def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        if n % i: i += 1
        else:
            n //= i
            factors[i] = factors.get(i, 0) + 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return factors

# 4. Pohlig-Hellman Algorithm
def pohlig_hellman(g, h, p):
    N = p - 1
    factors = prime_factors(N)
    
    remainders = []
    moduli = []
    
    for q, e in factors.items():
        q_e = q ** e
        moduli.append(q_e)
        
        x_mod_qe = 0
        gamma = h
        for i in range(e):
            term = pow(g, x_mod_qe, p)
            inv_term = modInverse(term, p)
            if inv_term is None: return None
            
            gamma_scaled = (gamma * inv_term) % p
            exponent = N // (q ** (i + 1))
            val = pow(gamma_scaled, exponent, p)
            
            g_q = pow(g, N // q, p)
            
            x_i = None
            # Small step brute-force up to q since q is a small factor
            for j in range(q + 1):
                if pow(g_q, j, p) == val:
                    x_i = j
                    break
            
            if x_i is None:
                return None
            x_mod_qe += x_i * (q ** i)
            
        remainders.append(x_mod_qe)
        
    ans = crt(remainders, moduli)
    if pow(g, ans, p) == h:
        return ans
    return None

# --- Benchmarking / Testing Suite ---
def run_test(name, g, x_true, p):
    print(f"\n=============================================")
    print(f"--- Test: {name} | Modulus p = {p} ---")
    h = pow(g, x_true, p)
    print(f"Goal: Find independent x such that {g}^x = {h} mod {p}")
    print(f"Expected Answer: {x_true}")
    print(f"---------------------------------------------")
    
    algorithms = [
        ("Brute Force         ", brute_force),
        ("Baby-step Giant-step", bsgs),
        ("Pollard's Rho       ", pollards_rho),
        ("Pohlig-Hellman      ", pohlig_hellman)
    ]
    
    for algo_name, func in algorithms:
        try:
            start_time = time.perf_counter()
            res = func(g, h, p)
            end_time = time.perf_counter()
            
            status = "PASSED" if (res is not None and pow(g, res, p) == h) else f"FAILED (got {res})"
            print(f"[{status}] {algo_name} | Time taken: {end_time - start_time:.6f} seconds")
        except Exception as e:
             print(f"[ERROR ] {algo_name} | Exception: {str(e)}")

if __name__ == "__main__":
    print("Testing Cryptographic Algorithms for Discrete Logarithm Problem...")
    # Test 1: 16-bit prime 
    run_test("Tiny Prime (16-bit)", g=3, x_true=1543, p=65537)
    
    # Test 2: 20-bit prime
    run_test("Small Prime (20-bit)", g=2, x_true=45678, p=1048583)
    
    # Test 3: 24-bit prime
    run_test("Medium Prime (24-bit)", g=5, x_true=1234567, p=16777259)
    
    # Test 4: Pohlig-Hellman specialized weak prime
    # Modulus 106696591 is a 26-bit prime.
    # Its group order p-1 = 106696590 = 2 * 3 * 5 * 7 * 11 * 11 * 13 * 17 * 19 (extremely smooth)
    run_test("Smooth/Weak Prime (26-bit)", g=7, x_true=1234567, p=106696591)
    
    print("\nBenchmark Complete!")
