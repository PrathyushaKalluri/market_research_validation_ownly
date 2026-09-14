"""Statistical helpers tied to the pre-analysis plan (PAP section 5).

All random procedures take an explicit numpy Generator seeded from config.SEED.
"""
from math import sqrt
import numpy as np
import pandas as pd
from scipy import stats

import config as C

Z = 1.959963984540054


def rng(offset=0):
    return np.random.default_rng(C.SEED + offset)


# ---------------------------------------------------------------- proportions
def wilson(k, n, z=Z):
    if n is None or n == 0 or pd.isna(n):
        return (np.nan, np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (p, (c - m) / d, (c + m) / d)


def newcombe_diff(k1, n1, k2, n2):
    """Newcombe hybrid-score CI for p1 - p2 (independent samples)."""
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    d = p1 - p2
    lo = d - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, lo, hi


def two_prop_test(k1, n1, k2, n2):
    table = np.array([[k1, n1 - k1], [k2, n2 - k2]])
    expected = stats.contingency.expected_freq(table)
    if (expected < 5).any():
        return "fisher_exact", stats.fisher_exact(table)[1]
    p = (k1 + k2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (k1 / n1 - k2 / n2) / se if se > 0 else 0.0
    return "two_prop_z", 2 * (1 - stats.norm.cdf(abs(z)))


def mcnemar_paired(a, b):
    """a, b: 0/1 arrays for the same respondents. Exact McNemar + paired diff CI (Wald, Agresti-Min adj.)."""
    a = np.asarray(a).astype(int)
    b = np.asarray(b).astype(int)
    n = len(a)
    b01 = int(((a == 1) & (b == 0)).sum())
    b10 = int(((a == 0) & (b == 1)).sum())
    disc = b01 + b10
    p = stats.binomtest(b01, disc, 0.5).pvalue if disc > 0 else 1.0
    # Agresti-Min adjusted Wald CI for paired difference
    na = n + 2
    d = (b01 + 0.5 - (b10 + 0.5)) / na
    se = sqrt(((b01 + 0.5) + (b10 + 0.5) - ((b01 + 0.5) - (b10 + 0.5)) ** 2 / na) / na ** 2)
    return {"diff": (b01 - b10) / n if n else np.nan, "ci_low": d - Z * se, "ci_high": d + Z * se,
            "p": p, "n": n, "discordant": disc}


# ---------------------------------------------------------------- location
def boot_median_ci(x, n_boot=None, seed_offset=0):
    x = pd.Series(x).dropna().to_numpy(dtype=float)
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    n_boot = n_boot or C.N_BOOT
    g = rng(seed_offset)
    idx = g.integers(0, len(x), size=(n_boot, len(x)))
    meds = np.median(x[idx], axis=1)
    return (float(np.median(x)), *np.percentile(meds, [2.5, 97.5]))


def cluster_boot_stat(df, col, cluster, func=np.median, n_boot=None, seed_offset=0):
    d = df[[col, cluster]].dropna()
    if d.empty:
        return (np.nan, np.nan, np.nan)
    groups = [g[col].to_numpy(dtype=float) for _, g in d.groupby(cluster)]
    g_rng = rng(seed_offset)
    n_boot = n_boot or C.N_BOOT_AUDIT
    vals = []
    for _ in range(n_boot):
        pick = g_rng.integers(0, len(groups), size=len(groups))
        vals.append(func(np.concatenate([groups[i] for i in pick])))
    return (float(func(d[col].to_numpy(dtype=float))), *np.percentile(vals, [2.5, 97.5]))


def mann_whitney(x, y):
    x = pd.Series(x).dropna().to_numpy(float)
    y = pd.Series(y).dropna().to_numpy(float)
    if len(x) == 0 or len(y) == 0:
        return {"U": np.nan, "p": np.nan, "r_rb": np.nan, "hl_shift": np.nan, "n1": len(x), "n2": len(y)}
    u, p = stats.mannwhitneyu(x, y, alternative="two-sided")
    r_rb = 2 * u / (len(x) * len(y)) - 1          # >0 means x tends to be larger
    hl = float(np.median(np.subtract.outer(x, y)))
    return {"U": float(u), "p": float(p), "r_rb": float(r_rb), "hl_shift": hl, "n1": len(x), "n2": len(y)}


def wilcoxon_paired(x, y):
    d = (pd.Series(x) - pd.Series(y)).dropna()
    d = d[d != 0]
    if len(d) < 5:
        return {"W": np.nan, "p": np.nan, "r_mp": np.nan, "n": len(d)}
    w, p = stats.wilcoxon(d)
    ranks = stats.rankdata(d.abs())
    r_mp = (ranks[d > 0].sum() - ranks[d < 0].sum()) / ranks.sum()   # matched-pairs rank-biserial
    return {"W": float(w), "p": float(p), "r_mp": float(r_mp), "n": len(d)}


def chi2_or_fisher(a, b):
    t = pd.crosstab(a, b)
    if t.shape[0] < 2 or t.shape[1] < 2:
        return {"test": "none", "p": np.nan, "cramers_v": np.nan, "n": int(t.values.sum())}
    chi2, p, dof, exp = stats.chi2_contingency(t, correction=False)
    n = t.values.sum()
    v = sqrt(chi2 / (n * (min(t.shape) - 1)))
    test = "chi_square"
    if (exp < 5).any():
        if t.shape == (2, 2):
            p = stats.fisher_exact(t.values)[1]
            test = "fisher_exact"
        else:
            res = stats.chi2_contingency(t, correction=False)
            test = "chi_square_sparse_warning"
    return {"test": test, "p": float(p), "cramers_v": float(v), "n": int(n)}


def spearman_boot(x, y, n_boot=None, seed_offset=0):
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(d) < 5:
        return {"rho": np.nan, "ci_low": np.nan, "ci_high": np.nan, "p": np.nan, "n": len(d)}
    rho, p = stats.spearmanr(d.x, d.y)
    g = rng(seed_offset)
    n_boot = n_boot or min(C.N_BOOT, 2000)
    arr = d.to_numpy()
    vals = []
    for _ in range(n_boot):
        s = arr[g.integers(0, len(arr), len(arr))]
        vals.append(stats.spearmanr(s[:, 0], s[:, 1])[0])
    lo, hi = np.nanpercentile(vals, [2.5, 97.5])
    return {"rho": float(rho), "ci_low": float(lo), "ci_high": float(hi), "p": float(p), "n": len(d)}


def cronbach_alpha(items: pd.DataFrame):
    d = items.dropna()
    k = d.shape[1]
    if len(d) < 10 or k < 2:
        return np.nan
    var_sum = d.var(ddof=1).sum()
    total_var = d.sum(axis=1).var(ddof=1)
    return float(k / (k - 1) * (1 - var_sum / total_var)) if total_var > 0 else np.nan


# ---------------------------------------------------------------- decisions
def holm(pvals):
    """Holm-Bonferroni adjusted p-values (NaNs kept)."""
    p = pd.Series(pvals, dtype=float)
    ok = p.dropna().sort_values()
    m = len(ok)
    adj = pd.Series(np.nan, index=p.index)
    running = 0.0
    for i, (idx, val) in enumerate(ok.items()):
        running = max(running, min(1.0, (m - i) * val))
        adj[idx] = running
    return adj.tolist()


def verdict_ci(lo, hi, threshold, direction="greater", n=None, min_n=None):
    """Universal rule (hypothesis tree section 0)."""
    if min_n is not None and (n is None or n < min_n):
        return "NOT TESTABLE"
    if pd.isna(lo) or pd.isna(hi):
        return "NOT TESTABLE"
    if direction == "greater":
        if lo > threshold:
            return "SUPPORTED"
        if hi < threshold:
            return "REJECTED"
    else:
        if hi < threshold:
            return "SUPPORTED"
        if lo > threshold:
            return "REJECTED"
    return "INCONCLUSIVE"


def rescale_1_5(x):
    return (pd.to_numeric(x, errors="coerce") - 1) / 4 * 100
