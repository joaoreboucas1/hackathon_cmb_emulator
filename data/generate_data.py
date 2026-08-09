from math import exp
import camb
from scipy.stats.qmc import LatinHypercube, scale

# Cosmology array:
# [h, omch2, ombh2, ln(10^10*As), ns, tau]
lower_bounds = [0.2, 0.001, 0.005, 1.61, 0.7, 0.01]
upper_bounds = [1.0, 0.99,  0.04,  5.0,  1.3, 0.4 ]

def get_cmb_spectra(cosmo):
    h, omch2, ombh2, lnAs1e10, ns, tau = cosmo
    As = 1e-10*exp(lnAs1e10)
    pars = camb.set_params(
        H0=100*h, omch2=omch2, ombh2=ombh2, As=As, ns=ns, tau=tau, mnu=0, halofit_version="mead", lmax=3000
    )
    results = camb.get_results(pars)
    cl_tt, cl_ee, _, cl_te = results.get_cmb_power_spectra(lmax = 3000, CMB_unit="muK")["total"].T
    cl_pp = results.get_lens_potential_cls(lmax = 3000, CMB_unit="muK")[:, 0]
    return cl_tt[2:], cl_te[2:], cl_ee[2:], cl_pp[2:]

if __name__ == "__main__":
    sampler = LatinHypercube(d=len(lower_bounds))
    samples = scale(sampler.random(n=1_000), lower_bounds, upper_bounds)
    for sample in samples:
        print(sample)
        try:
            cl_tt, cl_te, cl_ee, cl_pp = get_cmb_spectra(sample)
        except camb.baseconfig.CAMBError as e:
            print("Error!!")
            exit(1)
    # print(cl_pp)

