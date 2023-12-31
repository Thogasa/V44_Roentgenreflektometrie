from pickle import TRUE
import string
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as up
import uncertainties as un
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)

def sigFig(x):
    return -int(np.floor(np.log10(np.abs(x)))) 

def parratt(a_i, del2, del3, sig1, sig2,b2,b3, d2):
    a_irad = np.deg2rad(a_i)

    b2 = b2*1j
    b3 = b3*1j

    k = 2 * np.pi / 1.541e-10

    n2 = 1-del2 + b2
    n3 = 1-del3 + b3

    kz1 = k * np.sqrt(1 - np.cos(a_irad) **2)
    kz2 = k * np.sqrt(n2**2 - np.cos(a_irad)**2)
    kz3 = k * np.sqrt(n3**2 - np.cos(a_irad)**2)

    phase12 = np.exp(-2*kz1*kz2 * sig1 **2)
    phase23 = np.exp(-2*kz2*kz3 * sig2 **2)
    
    r12 = (kz1-kz2)/(kz1+kz2) * phase12
    r23 = (kz2-kz3)/(kz2+kz3) * phase23

    x2 = np.exp(-2j*kz2*d2)*r23
    x1 = (r12 + x2)/ (1 + r12 * x2)

    return np.abs(x1)**2
    

    


def generateplot(x,y,  xlabel:string, ylabel:string, name: string, islog: bool):
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['font.size'] = 16
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['text.usetex'] = 1


    
    yCor = []
    for xi,yi in zip(x,y):
        if(xi < 1.777):
            G =np.sin(np.deg2rad(xi))*20/0.62
            yCor.append(yi/G)
        else:
            yCor.append(yi)
    print(np.where(x == 0.225)[0])
    normFak = yCor[np.where(x == 0.225)[0][0]]
    yCor = [i/normFak for i in yCor]

    y = []
    for xi,yi in zip(x,yCor):
        if(xi < 1.777):
            G =np.sin(np.deg2rad(xi))*20/0.62
            y.append(yi*G)
        else:
            y.append(yi)
    
    pars =  [7.6e-06, 8.077e-6, 2.688e-9, 4.829e-10, 3.863e-7, 1.483e-5, 8.139e-08]
    pars = [8.912087912087914e-06, 3.5861738261738266e-06, 4.665934065934067e-09, 5.810897702297702e-10, 
            5.337472527472534e-08, 2.84021978021978e-06, 6.819180819180819e-08]
    
    reflectivity = parratt(x, *pars)
    

    plt.plot(x, reflectivity, color = 'g')

    
    plt.plot(x, yCor, color = 'r', label='Geometriefaktor korrigierte Messdaten')
    
    print(np.rad2deg(np.sqrt(2*pars[0])))
    
    print(np.rad2deg(np.sqrt(2*pars[1])))

    plt.axvline(np.rad2deg(np.sqrt(2*pars[0])), color = 'cyan', linestyle = 'dashdot', label = r"$\alpha_{C, Polyterol}$")
    plt.axvline(np.rad2deg(np.sqrt(2*pars[1])), color = 'pink', linestyle = 'dashdot', label = r"$\alpha_{C, Silizium}$")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(islog):
        plt.yscale('log')
    plt.yticks([1e2, 1e0, 1e-2, 1e-4, 1e-6])
    
    plt.legend(loc='best')
    # plt.ylim(1e-11, 1)
    plt.grid(True)
    plt.savefig("build/plot" + name + ".pdf")
    plt.clf()


data = np.loadtxt("build/Scan_6_Oszillation_bei_0.txt")
data1 = np.loadtxt("build/Scan_7_Oszillation_bei_0,1.txt")



data = np.array([[d[0], d[1]-d1[1]] for d, d1 in zip(data, data1)])
normFak = data[np.where(data[:,0] == 0.225)[0],1][0]
print(normFak)

# data = np.array([[d[0],d[1]/normFak] for d in data])

x = data[:,0]
y = data[:,1]


# Print the calculated reflectivity values
generateplot(x, y, r'$\alpha$ in $°$', 'Reflektivität', 'parratt', True)
