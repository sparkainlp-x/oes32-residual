# ADR-001 — Unify OES-32 residual / latch thresholds

- **Status:** Accepted — Option A (Residual-canonical)
- **Date decided:** 2026-09-20 (America/Toronto)
- **Owner:** Jean-François Brisson / Spark AI NLP
- **Repos:** sparkainlp-x (oes32-residual, oes32_engine, oes32-hls, oes512-residual)

## Decision

**Option A — Residual-canonical** is the public science path.

1. `oes32-residual` (pin: `b77b61254f15778c6ae221843dceac7a8571158e` until superseded) is the only normative residual definition:
   - Inputs: two finite length-32 real vectors + finite non-negative tolerance
   - Component residual: `|obs[i] - ref[i]|`
   - Aggregate R: max of the 32 component residuals
   - Fail iff R > tolerance; invalid input → `ValueError`, no status
2. **Profile A sidecars (locked 2026-09-20 by founder direction “do what is more logical”):** `oes32_engine` / `oes32-hls` call/import the residual contract for R, then apply named sidecar checks (EVEN/ODD, FOLD8) with separately versioned `τ_sym` / `τ_fold`. Do not invent a second product name. Document each sidecar τ explicitly in README.
3. OES-512 weighted latch `S = 0.45·Peak + 0.35·RMS + 0.20·MeanAbs` with default τ = 0.50 remains **TARGET / unpublished** until source + seed-42 fixtures ship. Do not cite as public fact.
4. No silent default τ in partner prose; every binary/README prints the tolerance or profile it uses.
5. Hilbert feature encode and Cf/K/D/Ψ/Omega remain software sidecars **after** classical latch; never marketed as hardware Hilbert capacity.

## Admit / latch bits (post-decision)

| Bit | Value |
|---|---|
| Residual contract public | 1 |
| τ unification path chosen | 1 (Option A) |
| Profile A sidecars chosen | 1 |
| Engine/HLS aligned to A | 1 (both READMEs cite oes32-residual and are labelled Profile A sidecars; see "Definitional differences" below) |
| Weighted S@0.50 public | 0 |
| QPU / medical / flight claims | 0 (latched closed) |

## Non-goals

Do not map this decision to a physical qubit gate, QPU, surface code, treatment, or certification. Do not promote HLS “&lt;20 ns” or qldpc microbench ns as product decoder latency.

## Follow-on work

1. Engine README: cite oes32-residual SHA; label τ=0.08 as Profile A sidecar (`τ_coherence` or equivalent); EVEN/ODD + FOLD8 as named sidecars.
2. HLS README: same; retag latency as TARGET until synth report exists; add LICENSE file.
3. Publish JSON Schema + golden vectors under oes32-residual.
4. CLAIM_HYGIENE.md + forbidden-phrase CI.
5. Demo repo: METRIC_TAG=SYNTHETIC; kill Investor/QECC overclaim framing.

## Definitional differences across implementations (documented 2026-09-26)

The three repositories that use the name "OES-32" do **not** compute the same residual or apply the same failure rule. This is intentional under Option A (only `oes32-residual` is normative) and is documented here so reviewers do not read it as an undetected inconsistency.

| | oes32-residual (**normative**, `b77b612`) | oes32_engine (Profile A sidecar) | oes32-hls (Profile A sidecar, TARGET) |
|---|---|---|---|
| Residual | `max |obs[i] − ref[i]|` | `max |x[i] − x_ref[i]|` (matches normative R) | `max |p[i] − r[i]|²` — **squared** difference |
| Threshold | caller-supplied tolerance | τ_coherence = 0.08 (default) | τ = 0.09 (`COHERENCE_TAU`) |
| Fail rule | fail iff R **>** tol (equality passes) | latch iff R **>** τ (equality passes) | fail iff sq **≥** τ (equality **fails**; pass iff sq < τ) |
| Symmetry | n/a | mirrored-index S_p, μ(i) = (i+16) mod 32 | `|Σ even − Σ odd|` ≥ τ fails |
| FOLD8 | n/a | adjacent-node differences in contiguous 8-blocks | ring sums over strided indices (i mod 4), `|ring_sum|` ≥ τ fails |

### Consequences of the HLS definition

- **Squared vs. absolute:** HLS compares the *squared* component difference to τ = 0.09. For non-negative values, `d² ≥ 0.09` ⇔ `|d| ≥ 0.3`, so the HLS coherence floor is equivalent to an absolute-difference threshold of **0.3**, not 0.09. It is not numerically comparable to the engine's 0.08 or to a normative tolerance of 0.09.
- **≥ vs. >:** HLS fails at equality (`sq ≥ τ`); the normative contract and the engine pass at equality (`R > tol` fails). A vector exactly at the threshold is PASS in `oes32-residual` / `oes32_engine` and FAIL in `oes32-hls`.
- **Status:** these HLS definitions are a Profile A sidecar and **TARGET** co-design exploration. They are not normative and are not bit-matched to the Python reference. Any future alignment (for example, computing `|d|` and using `>`), must be a separately reviewed change with updated testbench cases (TC5/TC6 currently encode the `≥` boundary).

## Red Team stamp

PASS — Option A named; weighted S not claimed public; residual FAIL-CLOSED preserved.
