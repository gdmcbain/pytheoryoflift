from matplotlib.pyplot import subplots
import numpy as np
from pandas import DataFrame
from scipy.constants import kilo

from pytheoryoflift.air import atmosphere


def figure1_7():
    y = np.linspace(0, 20e3)
    p, T, rho, a, mu = atmosphere(y)
    properties = ["p", "T", r"\rho", "a", r"\mu"]
    atm = DataFrame(dict(zip(properties, atmosphere(y))), index=y)
    sea_level = atm.loc[0.0]
    print(atm / sea_level)
    print("sea level:", sea_level)

    fig, ax = subplots()
    ax.set_title(
        "Figure 1.7 Relative variation of the lower International Standard Atmosphere with altitude"
    )
    ax.set_xlabel("Properties relative to those at sea level")
    ax.set_ylabel(r"Altitude, $y$ / km")
    yticks = np.linspace(0, 20, 5)
    ax.set_yticks(yticks, [f"{y:.0f}" for y in yticks])
    for property in ["p", r"\rho", "T", r"\mu", "a"]:
        ax.plot((atm / sea_level)[property], y / kilo, label=r"$%s$" % property)
    ax.legend(loc=3)
    fig.savefig("figure1.7.png")


if __name__ == "__main__":
    figure1_7()
