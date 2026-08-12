from math import exp
import numpy as np
import camb
from scipy.stats.qmc import LatinHypercube, Sobol, scale
import matplotlib.pyplot as plt
from itertools import combinations

# Cosmology array:
# [h, omch2, ombh2, ln(10^10*As), ns, tau]
lower_bounds = [0.6, 0.05, 0.01, 2.0, 0.8, 0.01]
upper_bounds = [0.8, 0.20, 0.03, 4.0, 1.1, 0.25]
param_labels = ["h", "omch2", "ombh2", "ln(10^10 As)", "ns", "tau"]

def get_cmb_spectra(cosmo):
    h, omch2, ombh2, lnAs1e10, ns, tau = cosmo
    As = 1e-10*exp(lnAs1e10)
    pars = camb.set_params(
        H0=100*h, omch2=omch2, ombh2=ombh2, As=As, ns=ns, tau=tau, mnu=0, halofit_version="mead", lmax=3000
    )
    results = camb.get_results(pars)
    cl_tt, cl_ee, _, cl_te = results.get_cmb_power_spectra(lmax=3000, CMB_unit="muK")["total"].T
    # cl_pp = results.get_lens_potential_cls(lmax=3000, CMB_unit="muK")[:, 0]
    return cl_tt[2:], cl_te[2:], cl_ee[2:]


def plot_pairwise_samples(samples, errors, labels, filename="pairwise_scatter.png"):
    n_params = samples.shape[1]
    pair_indices = list(combinations(range(n_params), 2))
    n_plots = len(pair_indices)
    n_cols = 3
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3 * n_rows), constrained_layout=True)
    axes = axes.reshape(-1)

    for ax, (i, j) in zip(axes, pair_indices):
        ax.scatter(samples[~errors, i], samples[~errors, j], c="green", marker="o", label="success", edgecolors="black", s=45, alpha=0.5)
        ax.scatter(samples[errors, i], samples[errors, j], c="red", marker="x", label="CAMBError", s=45, alpha=0.5)
        ax.set_xlabel(labels[i])
        ax.set_ylabel(labels[j])
        ax.tick_params(axis="both", which="major", labelsize=8)
        ax.legend(fontsize=7, loc="best")

    for ax in axes[len(pair_indices):]:
        fig.delaxes(ax)

    fig.suptitle("Projected 2D parameter samples by CAMB outcome", fontsize=14)
    fig.savefig(filename, dpi=150)
    print(f"Saved pairwise scatter figure to {filename}")


if __name__ == "__main__":
    NUM_SAMPLES = 512
    data_path = "./data/train_512_sobol/"
    # sampler = LatinHypercube(d=len(lower_bounds))
    sampler = Sobol(d=len(lower_bounds))
    all_samples = scale(sampler.random(n=NUM_SAMPLES), lower_bounds, upper_bounds)
    samples = []
    errors = []
    num_errors = 0
    sample_counter = 0
    for sample in all_samples:
        try:
            data = get_cmb_spectra(sample)
            data = np.column_stack(data)
            sample_counter += 1
            if sample_counter%10 == 0: print(f"Sample {sample_counter}")
            np.savetxt(f"{data_path}/cl_{sample_counter}.txt", data, header="cl_TT                  cl_TE                    cl_EE")
            samples.append(sample)
            errors.append(False)
        except camb.baseconfig.CAMBError:
            errors.append(True)
            num_errors += 1

    np.savetxt(f"{data_path}/cosmologies.txt", samples, header="h        omch2      ombh2      ln(10^10*As)    ns    tau", fmt="%.8f")
    errors = np.array([bool(e) for e in errors])
    print(f"Error rate: {num_errors/len(all_samples):.3f}")
    # plot_pairwise_samples(samples, errors, param_labels)

