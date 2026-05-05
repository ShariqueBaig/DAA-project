"""
Discrete Logarithm Problem - Core Algorithm Implementations
4 algorithms: Brute Force, BSGS, Pollard's Rho, Pohlig-Hellman
"""

import math
import random
import time

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def egcd(a, b):
    """Extended Euclidean algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modinv(a, m):
    """Modular inverse using extended Euclidean algorithm"""
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        return None
    return x % m

def prime_factors(n):
    """Return prime factorization as dictionary {prime: exponent}"""
    factors = {}
    i = 2
    while i * i <= n:
        if n % i == 0:
            cnt = 0
            while n % i == 0:
                n //= i
                cnt += 1
            factors[i] = cnt
        i += 1 if i == 2 else 2
    if n > 1:
        factors[n] = 1
    return factors

def crt(remainders, moduli):
    """Chinese Remainder Theorem solver"""
    total = 0
    prod = 1
    for m in moduli:
        prod *= m
    for r, m in zip(remainders, moduli):
        p = prod // m
        total += r * modinv(p, m) * p
    return total % prod

def is_primitive_root(g, p, factors):
    """Check if g is a primitive root modulo p"""
    for q in factors.keys():
        if pow(g, (p-1)//q, p) == 1:
            return False
    return True

def find_primitive_root(p):
    """Find a primitive root modulo prime p"""
    if p == 2:
        return 1
    factors = prime_factors(p-1)
    for g in range(2, min(100, p)):
        if is_primitive_root(g, p, factors):
            return g
    return 2  # fallback

# ============================================================================
# ALGORITHM 1: BRUTE FORCE
# ============================================================================

def brute_force(g, h, p, timeout=600):
    """
    Sequential brute force search
    Time: O(p), Space: O(1)
    """
    start_time = time.perf_counter()
    
    for x in range(p):
        # Check timeout
        if (time.perf_counter() - start_time) > timeout:
            return None, "TIMEOUT"
        
        if pow(g, x, p) == h:
            return x, "PASSED"
    
    return None, "FAILED"

# ============================================================================
# ALGORITHM 2: BABY-STEP GIANT-STEP (BSGS)
# ============================================================================

def bsgs(g, h, p, timeout=600):
    """
    Baby-step Giant-step algorithm
    Time: O(√p), Space: O(√p)
    """
    start_time = time.perf_counter()
    order = p - 1
    m = math.isqrt(order) + 1
    
    # Baby steps: store g^j
    table = {}
    curr = 1
    for j in range(m):
        # Check timeout during precomputation
        if (time.perf_counter() - start_time) > timeout:
            return None, "TIMEOUT"
        
        if curr not in table:
            table[curr] = j
        curr = (curr * g) % p
    
    # Giant steps: h * (g^{-m})^i
    gm = pow(g, m, p)
    inv_gm = modinv(gm, p)
    if inv_gm is None:
        return None, "FAILED"
    
    curr = h
    for i in range(m):
        # Check timeout during search
        if (time.perf_counter() - start_time) > timeout:
            return None, "TIMEOUT"
        
        if curr in table:
            result = i * m + table[curr]
            if pow(g, result, p) == h:
                return result, "PASSED"
        curr = (curr * inv_gm) % p
    
    return None, "FAILED"

# ============================================================================
# ALGORITHM 3: POLLARD'S RHO
# ============================================================================

def pollards_rho(g, h, p, timeout=600):
    """
    Pollard's Rho algorithm for discrete log
    Time: O(√p) expected, Space: O(1)
    """
    start_time = time.perf_counter()
    order = p - 1
    
    def f(x, a, b):
        """Pseudorandom function for the walk"""
        r = x % 3
        if r == 0:
            return (x * x) % p, (a * 2) % order, (b * 2) % order
        elif r == 1:
            return (x * g) % p, (a + 1) % order, b
        else:
            return (x * h) % p, a, (b + 1) % order
    
    # Try multiple random starting points
    for attempt in range(5):
        # Check global timeout
        if (time.perf_counter() - start_time) > timeout:
            return None, "TIMEOUT"
        
        # Random starting point
        a = random.randint(1, order)
        b = random.randint(1, order)
        x = (pow(g, a, p) * pow(h, b, p)) % p
        
        # Tortoise and hare
        x_t, a_t, b_t = x, a, b
        x_h, a_h, b_h = x, a, b
        
        for _ in range(order):
            # Check timeout during iteration
            if (time.perf_counter() - start_time) > timeout:
                return None, "TIMEOUT"
            
            # Tortoise: one step
            x_t, a_t, b_t = f(x_t, a_t, b_t)
            # Hare: two steps
            x_h, a_h, b_h = f(x_h, a_h, b_h)
            x_h, a_h, b_h = f(x_h, a_h, b_h)
            
            if x_t == x_h:
                break
        
        # Solve for the exponent
        db = (b_t - b_h) % order
        if db == 0:
            continue
        
        da = (a_h - a_t) % order
        gcd, inv, _ = egcd(db, order)
        
        if da % gcd != 0:
            continue
        
        inv_db = modinv(db // gcd, order // gcd)
        if inv_db is None:
            continue
        
        x = (da // gcd * inv_db) % (order // gcd)
        
        # Verify
        for k in range(gcd):
            candidate = (x + k * (order // gcd)) % order
            if pow(g, candidate, p) == h:
                return candidate, "PASSED"
    
    return None, "FAILED"

# ============================================================================
# ALGORITHM 4: POHLIG-HELLMAN (SIMPLIFIED, CORRECTED)
# ============================================================================

def pohlig_hellman(g, h, p, timeout=600):
    """
    Pohlig-Hellman algorithm using CRT
    Fast when p-1 has small prime factors
    """
    start_time = time.perf_counter()
    order = p - 1
    factors = prime_factors(order)
    
    remainders = []
    moduli = []
    
    for q, e in factors.items():
        # Check timeout
        if (time.perf_counter() - start_time) > timeout:
            return None, "TIMEOUT"
        
        qe = q ** e
        moduli.append(qe)
        
        # Solve x ≡ x_i (mod q^e)
        x_mod = 0
        gamma = h
        
        for i in range(e):
            # Check timeout per iteration
            if (time.perf_counter() - start_time) > timeout:
                return None, "TIMEOUT"
            
            # Compute gamma^(order/q^(i+1))
            exp = order // (q ** (i+1))
            gamma_pow = pow(gamma, exp, p)
            
            # Compute g^(order/q)
            g_pow = pow(g, order // q, p)
            
            # Solve discrete log in subgroup of order q
            # For q small: brute force
            # For q larger but still moderate: use baby-step giant-step
            x_i = None
            
            if q <= 10000:  # Small enough for brute force
                for j in range(q):
                    if pow(g_pow, j, p) == gamma_pow:
                        x_i = j
                        break
            else:
                # Use BSGS for larger subgroups
                m = math.isqrt(q) + 1
                table = {}
                curr = 1
                for j in range(m):
                    if curr not in table:
                        table[curr] = j
                    curr = (curr * g_pow) % p
                
                gm = pow(g_pow, m, p)
                inv_gm = modinv(gm, p)
                if inv_gm is not None:
                    curr = gamma_pow
                    for j in range(m):
                        if curr in table:
                            x_i = j * m + table[curr]
                            break
                        curr = (curr * inv_gm) % p
            
            if x_i is None:
                return None, "FAILED"
            
            x_mod += x_i * (q ** i)
            
            # Update gamma for next iteration
            # gamma = gamma * g^{-x_i * q^i}
            inv_g = modinv(g, p)
            if inv_g is None:
                return None, "FAILED"
            gamma = (gamma * pow(inv_g, x_i * (q ** i), p)) % p
        
        remainders.append(x_mod)
    
    # Combine using CRT
    result = crt(remainders, moduli)
    
    if pow(g, result, p) == h:
        return result, "PASSED"
    return None, "FAILED"


# ============================================================================
# UTILITY: Generate test primes
# ============================================================================

def generate_prime(bits, max_attempts=5000):
    """Generate a random prime of given bit length"""
    from sympy import isprime, randprime
    lower = 1 << (bits - 1)
    upper = (1 << bits) - 1
    try:
        return randprime(lower, upper)
    except:
        # Fallback
        for _ in range(max_attempts):
            candidate = random.getrandbits(bits)
            candidate |= (1 << (bits - 1)) | 1  # Ensure odd and correct bit length
            if isprime(candidate):
                return candidate
    return None

def generate_smooth_prime(bits, max_seconds=60):
    """
    Generate a prime where p-1 has only small prime factors
    These are vulnerable to Pohlig-Hellman
    """
    from sympy import isprime
    
    # Small primes for building smooth numbers
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    
    start_time = time.perf_counter()
    
    while (time.perf_counter() - start_time) < max_seconds:
        # Build p-1 from small primes
        n = 1
        while n.bit_length() < bits - 2:
            n *= random.choice(small_primes)
        
        p = n + 1
        if p.bit_length() == bits and isprime(p):
            # Verify all prime factors are small
            factors = prime_factors(p-1)
            if all(f <= max(small_primes) for f in factors):
                return p
    
    return None

def generate_hard_prime(bits, max_attempts=100):
    """
    Generate a prime where p-1 has a large prime factor
    These are resistant to Pohlig-Hellman
    """
    from sympy import isprime
    
    for _ in range(max_attempts):
        # Generate safe prime: p = 2q + 1 where q is prime
        q = generate_prime(bits - 1)
        if q is None:
            continue
        p = 2 * q + 1
        if isprime(p):
            return p
    
    return generate_prime(bits)  # fallback