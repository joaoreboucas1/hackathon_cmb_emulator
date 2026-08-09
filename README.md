# CMB Emulator - Arizona Cosmology Hackathon

The challenge consists in emulating the CMB power spectra with less than 1% error.

## Datasets

The training and test datasets are located inside `data/`. The `train/` and `test/` folders contain
- A file `lhs.txt` containing a list of cosmological parameter samples (inputs). Each line is a different sample, and the columns refer to the cosmological parameters $[h, \omega_c, \omega_b, \ln(10^{10}A_s), n_s, \tau]$.
- Files `cl_1.txt`, `cl_2.txt`, etc. containing the CMB power spectra (outputs).

## Motivation

Monte Carlo Markov Chains are the workhorse of cosmological data analysis. They are already expensive computations, requiring thousands of CPU-hours to run. A single scientific project usually involves running some dozens of MCMCs during its lifetime. In this context, next-generation data will require more accurate predictions, making inference even more expensive[^1].

Emulators are machine learning techniques that can substitute numerical calculations based on pre-computed cases. While CAMB runs in O(1 second), machine learning emulators are highly parallelizable and able to run in O(1 millisecond). Reducing the runtime by three orders of magnitude makes MCMCs converge in minutes, and even enable users to run MCMCs locally instead of in an HPC. 

## References

- Cosmopower: https://arxiv.org/pdf/2106.03846