"""
Enhanced Pohlig-Hellman with Nested BSGS
Improves robustness for semi-smooth primes by using BSGS for subgroups.
Usage: python enhanced_pohlig_hellman.py
"""
import math
from dlp_algorithms import ext_gcd, modInverse, crt, prime_factors, bsgs

def pohlig_hellman_enhanced(g, h, p):
    """
    Enhanced Pohlig-Hellman that uses BSGS for subgroups when brute force is slow.
    """
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
            if inv_term is None:
                return None

            gamma_scaled = (gamma * inv_term) % p
            exponent = N // (q ** (i + 1))
            val = pow(gamma_scaled, exponent, p)

            g_q = pow(g, N // q, p)

            # Use BSGS if q is large (>100), otherwise brute force
            if q > 100:
                # Solve in subgroup using BSGS
                x_i = bsgs(g_q, val, p)
                if x_i is None:
                    return None
            else:
                # Brute force for small q
                x_i = None
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

def test_enhanced_ph():
    """Test enhanced PH on sample cases."""
    test_cases = [
        (3, 56755, 65537, 1543),      # Small prime
        (7, 23437265, 106696591, 1234567), # Smooth prime
    ]

    print("Testing Enhanced Pohlig-Hellman")
    print("=" * 50)

    for g, h, p, expected in test_cases:
        import time
        start = time.perf_counter()
        result = pohlig_hellman_enhanced(g, h, p)
        elapsed = time.perf_counter() - start

        print(f"\nTesting: {g}^x = {h} (mod {p})")
        print(f"Result: {result}, Expected: {expected}")
        print(f"Time: {elapsed:.6f}s")
        print(f"Correct: {result == expected}")

if __name__ == "__main__":
    test_enhanced_ph()