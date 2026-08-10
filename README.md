# CMB Emulator - Arizona Cosmology Hackathon

The challenge consists in emulating the CMB power spectra with less than 1% error.

## Datasets

The training and test datasets are located inside `data/`. The `train/` and `test/` folders contain:
- A file `cosmologies.txt` containing a list of cosmological parameter samples (inputs). Each line is a different sample, and the columns refer to the cosmological parameters $[h, \omega_c, \omega_b, \ln(10^{10}A_s), n_s, \tau]$.
- Files `cl_1.txt`, `cl_2.txt`, etc. containing the CMB power spectra (outputs), such that `cl_i.txt` is the power spectrum computed in the cosmology at line `i` of the `cosmologies.txt` file. Each column represent one of the CMB primary power spectra: the first column is the TT spectrum, the second column is the TE cross spectrum, and the third is the EE spectrum.
The training set contains 9864 cosmologies, while the test set contains 976 cosmologies.

The `data/generate_data.py` script is the code used to generate both the training and test datasets. This script is kept here for documentation purposes.

## Motivation

Monte Carlo Markov Chains are the workhorse of cosmological data analysis. They are already expensive computations, requiring thousands of CPU-hours to run. A single scientific project usually involves running some dozens of MCMCs during its lifetime. In this context, next-generation data will require more accurate predictions, making inference even more expensive[^1].

Emulators are machine learning techniques that can substitute numerical calculations based on pre-computed cases. While CAMB runs in O(1 second), machine learning emulators are highly parallelizable and able to run in O(1 millisecond). Reducing the runtime by three orders of magnitude makes MCMCs converge in minutes, and even enable users to run MCMCs locally instead of in an HPC.

There is a multitude of techniques that can be applied for this problem, and they can also be applied for a multitude of other problems.

## References

- Cosmopower: https://arxiv.org/pdf/2106.03846
- CMBolic: https://arxiv.org/abs/2606.07745
- Capse.jl: https://arxiv.org/abs/2307.14339v3
- OLÉ: https://arxiv.org/abs/2503.13183v1
- PolyCAMB: https://arxiv.org/abs/2507.02179v3