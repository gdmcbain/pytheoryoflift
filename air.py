#!/usr/bin/env python

'''

Based on Octave code in 'Theory of Lift'.

:author: G. D. McBain <gdmcbain@freeshell.org>

:created: 2014-04-29

'''

from __future__ import absolute_import, division, print_function

import numpy as np
import pandas as pd
from scipy.constants import g

R = 287.0                       # J/kg K (p. 9)
cpcv = 7/5                      # ratio of specific heats

    
def speed_of_sound(T):
    '''return the speed of sound in air in m/s

    :param: T, temperature in kelvins

    Listing 1.1, p. 10
    
    '''
    
    return np.sqrt(cpcv * T * R)


def viscosity(T):
    '''return the viscosity of air in Pa.s

    :param: T, temperature in kelvins
    
    Listing 1.2, p. 11
    
    '''

    return 1.495e-6 * np.sqrt(T) / (1 + 120 / T)


def atmosphere(y):
    '''return the properties of the atmosphere over a range of altitudes

    :param: y, numpy.ndarray of altitude in metres    

    :rval: p, T, rho, a, mu, corresponding values of pressure / Pa,
    temperature / K, density / [kg / m**3], speed of sound / [m / s],
    viscosity / [Pa / s]

    Listing 1.3, p. 13

    '''
    
    T0 = 15 + 273.15            # temperature / K
    p0 = 101325.0               # pressure / Pa

    L = 6.5e-3                  # lapse rate / [K / m]
    yt = 11e3                   # tropopause / m
    top = 20e3                  # top of stratosphere / m

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
    
    return p, T, p / (R * T), speed_of_sound(T), viscosity(T)


def figure1_7():

    y = np.linspace(0, 20e3)
    p, T, rho, a, mu = atmosphere(y)
    properties = ['p', 'T', r'\rho', 'a', r'\mu']
    atm = pd.DataFrame(dict(zip(properties, atmosphere(y))), index=y)
    sea_level = atm.ix[0.0]
    print(atm / sea_level)
    print('sea level:', sea_level)

    plt.figure()
    plt.title('Figure 1.7 Relative variation of the lower International Standard Atmosphere with altitude')
    plt.xlabel('Properties relative to those at sea level')
    plt.ylabel(r'Altitude, $y$ / km')
    for property in ['p', r'\rho', 'T', r'\mu', 'a']:
        plt.plot((atm / sea_level)[property], y, label=r'$%s$' % property)
    plt.legend(loc=3)
    plt.savefig('figure1.7.png')
    

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    figure1_7()

