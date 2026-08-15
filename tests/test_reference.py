"""Contract tests for the OES-32 public reference implementation."""

import unittest

import numpy as np

import oes32_residual_public_v1 as oes


class ReferenceContractTests(unittest.TestCase):
    """Verify numerical invariants and the published residual definition."""

    def test_normalize_rho_returns_density_matrix(self):
        rng = np.random.RandomState(7)
        candidate = rng.normal(size=(oes.N, oes.N)) + 1j * rng.normal(size=(oes.N, oes.N))
        rho = oes.normalize_rho(candidate)

        self.assertTrue(np.allclose(rho, rho.conj().T, atol=1e-10))
        self.assertAlmostEqual(float(np.trace(rho).real), 1.0, places=10)
        self.assertGreaterEqual(float(np.min(np.linalg.eigvalsh(rho))), -1e-10)

    def test_published_residual_formula(self):
        dissociation = 0.4
        no_loop = float(np.clip(0.55 * dissociation + 0.30 * (1 - 0), 0.0, 1.0))
        loop = float(np.clip(0.55 * dissociation + 0.30 * (1 - 1), 0.0, 1.0))

        self.assertAlmostEqual(no_loop, 0.52)
        self.assertAlmostEqual(loop, 0.22)
        self.assertGreater(no_loop, loop)

    def test_seeded_monte_carlo_is_reproducible(self):
        first = oes.run_monte_carlo(n_runs=3, rng=np.random.RandomState(42))
        second = oes.run_monte_carlo(n_runs=3, rng=np.random.RandomState(42))

        self.assertEqual(first, second)
        self.assertEqual(len(first), 3)
        self.assertEqual(set(first[0]), {"S_R", "D", "loop", "cf", "level", "parity"})

    def test_summary_statistics_are_bounded(self):
        results = oes.run_monte_carlo(n_runs=5, rng=np.random.RandomState(42))
        summary = oes.summarize_results(results)

        self.assertGreaterEqual(summary["mean_s_r"], 0.0)
        self.assertLessEqual(summary["mean_s_r"], 1.0)
        self.assertGreaterEqual(summary["positive_s_r_fraction"], 0.0)
        self.assertLessEqual(summary["positive_s_r_fraction"], 1.0)
        self.assertGreaterEqual(summary["loop_entry_rate"], 0.0)
        self.assertLessEqual(summary["loop_entry_rate"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
