"""

Based on Octave code in 'Theory of Lift'.

"""

import numpy as np
from scipy.constants import g, atm, convert_temperature

R = 287.0  # J/kg K (p. 9)
cpcv = 7 / 5  # ratio of specific heats

p0 = atm  # sea-level pressure / Pa


def speed_of_sound(T):
    """return the speed of sound in air in m/s

    :param: T, temperature in kelvins

    Listing 1.1, p. 10

    """

    return np.sqrt(cpcv * T * R)


def viscosity(T):
    """return the viscosity of air in Pa.s

    :param: T, temperature in kelvins

    Listing 1.2, p. 11

    """

    return 1.495e-6 * np.sqrt(T) / (1 + 120 / T)


def density(T, p=p0):
    """return the density of air in kg / m**3

    Not a separate listing in 'Theory of Lift' but part of atmosphere.

    """

    return p / (R * T)


def atmosphere(y):
    """return the properties of the atmosphere over a range of altitudes

    :param: y, numpy.ndarray of altitude in metres

    :rval: p, T, rho, a, mu, corresponding values of pressure / Pa,
    temperature / K, density / [kg / m**3], speed of sound / [m / s],
    viscosity / [Pa / s]

    Listing 1.3, p. 13

    """

    T0 = convert_temperature(15, "C", "K")

    L = 6.5e-3  # lapse rate / [K / m]
    yt = 11e3  # tropopause / m
    top = 20e3  # top of stratosphere / m

    troposphere = y <= yt
    strat = np.logical_and(np.logical_not(troposphere), y <= top)
    T = np.nan * np.empty(y.shape)
    p = T.copy()

    T[troposphere] = T0 - L * y[troposphere]
    Ts = T0 - L * yt
    T[strat] = Ts

    p[troposphere] = p0 * (T[troposphere] / T0) ** (g / L / R)
    pt = p0 * (Ts / T0) ** (g / L / R)
    p[strat] = pt * np.exp(g / R / Ts * (yt - y[strat]))

    return p, T, density(T, p), speed_of_sound(T), viscosity(T)
