"""
OES-32 Residual Claim – Public Minimal Implementation v1
Spark AI NLP | Atlantic Canada | August 2026

Implements the operational residual defined in the public technical note:
    S(R) = max(0, 0.55 * D + 0.30 * (1 - L))

This is the code released for independent scrutiny.
"""

import numpy as np
from datetime import datetime

N = 32
N_RUNS = 300


# -------------------------------------------------
# Core functions (minimal)
# -------------------------------------------------
def normalize_rho(rho):
    rho = 0.5 * (rho + rho.conj().T)
    evals, evecs = np.linalg.eigh(rho)
    evals = np.clip(evals.real, 1e-12, None)
    rho = evecs @ np.diag(evals) @ evecs.conj().T
    tr = np.trace(rho).real
    return rho / tr if abs(tr) > 1e-12 else np.eye(N, dtype=complex) / N


def coherent_fraction(rho):
    rho = 0.5 * (rho + rho.conj().T)
    off = np.abs(rho - np.diag(np.diag(rho).real))
    return min(1.0, float(np.sum(off)) / (N - 1.0))


def von_neumann_entropy(rho, tol=1e-12):
    evals = np.real(np.linalg.eigvalsh(0.5 * (rho + rho.conj().T)))
    evals = np.clip(evals, tol, None)
    evals /= np.sum(evals)
    return float(-np.sum(evals * np.log(evals + tol)))


def dissociation_metric(rho, delta=1.0):
    S = von_neumann_entropy(rho)
    K = max(0.0, 1.5 * delta - 0.8 * S)
    S_norm = S / np.log(N)
    return float(max(0.0, S_norm * (1.5 - min(K, 1.5))))


def build_hamiltonian(J, lam, gamma, delta, level, parity):
    H = np.zeros((N, N), dtype=complex)
    for i in range(N):
        H[i, i] = 0.4 * np.sin(2 * np.pi * i / N) + 0.08 * level
    scale = 1.0 + 0.12 * level
    for i in range(N):
        for j in range(i + 1, N):
            strength = J * np.exp(-0.09 * abs(i - j)) * scale
            H[i, j] = H[j, i] = strength
    holo = 1.0 + 0.18 * level + 0.06 * parity
    for i in range(N):
        for j in range(N):
            if i != j:
                H[i, j] += lam * 0.035 * holo / (1 + abs(i - j))
    for i in range(N):
        partner = (i + 7) % N
        H[i, partner] += gamma * 0.55 * (1.0 + 0.04 * parity)
        H[partner, i] += gamma * 0.55 * (1.0 + 0.04 * parity)
    for i in range(N):
        H[i, i] += delta * 0.25 * np.cos(2 * np.pi * i / N)
    return H


def evolve_rho(rho, H, dt=0.012, steps=25, noise_rate=0.06):
    for _ in range(steps):
        rho = 0.5 * (rho + rho.conj().T)
        comm = H @ rho - rho @ H
        rho = rho - 1j * (comm - comm.conj().T) / 2 * dt
        rho *= (1.0 - 0.5 * noise_rate * dt)
        mask = 1.0 - np.eye(N)
        rho *= (1.0 - noise_rate * dt * mask)
        max_off = 2.0 / N
        off = rho - np.diag(np.diag(rho))
        off = (np.clip(off.real, -max_off, max_off) +
               1j * np.clip(off.imag, -max_off, max_off))
        rho = np.diag(np.diag(rho).real) + off
        rho = normalize_rho(rho)
    return rho


def infinity_feedback(rho, eta=0.15, steps=60):
    history = []
    for _ in range(steps):
        k = max(0.0, 1.5 - 0.8 * von_neumann_entropy(rho))
        feedback = eta * k * 0.35 * (rho - np.eye(N) / N)
        rho = normalize_rho(rho + feedback)
        history.append(coherent_fraction(rho))
    final_cf = coherent_fraction(rho)
    stability = (1.0 - np.std(history[-20:]) / (np.mean(history[-20:]) + 1e-8)
                 if len(history) > 10 else 0.5)
    return rho, final_cf, float(np.clip(stability, 0.0, 1.0))


# -------------------------------------------------
# Single cycle (lean)
# -------------------------------------------------
def run_cycle(J=2.25, lam=2.85, gamma=1.85, delta=1.15,
              eta=0.19, noise=0.085, level=3, Psi0=0.55, parity=0):

    psi0 = np.ones(N, dtype=complex) / np.sqrt(N)
    rho = np.outer(psi0, psi0.conj())
    Psi = float(Psi0)
    current_level = int(level)
    parity = int(parity) % 2

    H = build_hamiltonian(J, lam, gamma, delta, current_level, parity)

    # Eureka
    evals, evecs = np.linalg.eigh(rho)
    rho = normalize_rho(evecs @ np.diag(np.clip(evals, 1e-8, 1.0)**0.82) @ evecs.conj().T)
    rho = evolve_rho(rho, H, noise_rate=noise)

    cf = coherent_fraction(rho)
    k = max(0.0, 1.5 * delta - 0.8 * von_neumann_entropy(rho))
    Psi = float(np.clip(Psi + 0.22 * Psi * (1 - Psi/1.6) * max(0, cf*k), 0, 1.6))

    # Crystallization + possible level change
    product = cf * max(Psi, 0.15)
    activation = 1.0 / (1.0 + np.exp(-18.0 * (product - 0.42)))
    power = 1.35 + 1.8 * activation
    evals, evecs = np.linalg.eigh(rho)
    rho = normalize_rho(evecs @ np.diag(np.clip(evals, 1e-6, 1.0)**power) @ evecs.conj().T)
    rho = evolve_rho(rho, H, steps=14, noise_rate=noise * 0.5)

    if activation > 0.28 and current_level < 8:
        current_level += 1
        if activation > 0.6:
            parity = 1 - parity
        H = build_hamiltonian(J, lam, gamma, delta, current_level, parity)

    # Short synergy + symmetry
    H_emp = np.zeros((N, N), dtype=complex)
    for i in range(N):
        p = (i + 7) % N
        H_emp[i, p] = H_emp[p, i] = gamma * 0.5
    rho = evolve_rho(rho, H_emp, dt=0.015, steps=12, noise_rate=0.0)
    rho = evolve_rho(rho, H, noise_rate=noise * 0.5)

    mirror = np.fliplr(np.flipud(rho))
    rho = normalize_rho(0.5 * (rho + mirror))
    rho = evolve_rho(rho, H, noise_rate=noise * 0.6)

    # Final feedback
    eta_eff = eta * (1.0 + 0.09 * (current_level - 3) + 0.04 * parity)
    rho_final, final_cf, stability = infinity_feedback(rho, eta=eta_eff)

    final_D = dissociation_metric(rho_final, delta)
    loop_entered = int((final_cf > 0.72) and (stability > 0.70) and
                       (max(0.0, 1.5*delta - 0.8*von_neumann_entropy(rho_final)) > 0.55))

    # === THE PUBLIC RESIDUAL DEFINITION ===
    S_R = float(np.clip(0.55 * final_D + 0.30 * (1 - loop_entered), 0.0, 1.0))

    return {
        "S_R": S_R,
        "D": final_D,
        "loop": loop_entered,
        "cf": final_cf,
        "level": current_level,
        "parity": parity
    }


# -------------------------------------------------
# Monte Carlo
# -------------------------------------------------
def run_monte_carlo(n_runs=N_RUNS, rng=None):
    """Run the reference Monte Carlo sweep with a supplied legacy NumPy RNG."""
    rng = np.random.RandomState() if rng is None else rng
    results = []
    for i in range(n_runs):
        params = {
            "J":     rng.uniform(1.9, 2.6),
            "lam":   rng.uniform(2.4, 3.2),
            "gamma": rng.uniform(1.5, 2.1),
            "delta": rng.uniform(0.95, 1.35),
            "eta":   rng.uniform(0.14, 0.24),
            "noise": rng.uniform(0.05, 0.12),
            "level": rng.randint(2, 5),
            "Psi0":  rng.uniform(0.40, 0.70),
            "parity": rng.randint(0, 2)
        }
        res = run_cycle(**params)
        results.append(res)
        if (i + 1) % 50 == 0:
            print(f"  completed {i+1}/{n_runs}")
    return results


def summarize_results(mc):
    """Calculate the published summary statistics for Monte Carlo results."""
    S_R = np.array([r["S_R"] for r in mc])
    L = np.array([r["loop"] for r in mc])
    return {
        "mean_s_r": float(np.mean(S_R)),
        "std_s_r": float(np.std(S_R)),
        "median_s_r": float(np.median(S_R)),
        "p05_s_r": float(np.quantile(S_R, 0.05)),
        "p95_s_r": float(np.quantile(S_R, 0.95)),
        "positive_s_r_fraction": float(np.mean(S_R > 0)),
        "loop_entry_rate": float(np.mean(L)),
    }


def main(n_runs=N_RUNS, seed=42):
    """Execute a deterministic reference run and print its summary."""
    print("OES-32 Residual Public v1")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Runs: {n_runs} | Dimension: {N}")
    print("Residual definition: S(R) = max(0, 0.55*D + 0.30*(1-L))")
    print("-" * 60)
    print("Running public Monte Carlo...")
    mc = run_monte_carlo(n_runs=n_runs, rng=np.random.RandomState(seed))
    print("Done.\n")

    summary = summarize_results(mc)
    print("=== Public Residual Results ===")
    print(f"Mean S(R)          : {summary['mean_s_r']:.4f} ± {summary['std_s_r']:.4f}")
    print(f"Median S(R)        : {summary['median_s_r']:.4f}")
    print(f"5% – 95% quantiles : [{summary['p05_s_r']:.4f}, {summary['p95_s_r']:.4f}]")
    print(f"Fraction S(R) > 0  : {summary['positive_s_r_fraction']*100:.1f}%")
    print(f"Loop entry rate    : {summary['loop_entry_rate']*100:.1f}%")
    print()
    print("Residual definition used (exact):")
    print("  S(R) = max(0, 0.55 * D + 0.30 * (1 - L))")
    return mc, summary


if __name__ == "__main__":
    main()
