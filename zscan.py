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

def gauss(x,a,mu,sig):
    return a*np.exp(-((x-mu)/sig)**2)

def sigFig(x):
    return -int(np.floor(np.log10(np.abs(x))))

def generateplot(x,y,  xlabel:string, ylabel:string, name: string, islog: bool,):
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['font.size'] = 16
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['text.usetex'] = 1
    

    x_plot = np.linspace(x[0], np.max(x), 150)
    
    plt.plot(x,y,'o', color = "b",label ="Messdaten")    
    
    plt.axvline(x[78] , color = 'r', linestyle = 'dashdot')
    plt.axvline(x[140], color = 'r', linestyle = 'dashdot')
    

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(islog):
        plt.yscale('log')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig("build/plot" + name + ".pdf")
    plt.clf()

    print(np.where(x==-0.22))
    print(np.where(x== 0.4))
    width = x[140] - x[78]



    f = open("build/erg" + name + ".tex","w")
    f.write(r"\begin{equation*}" + "\n")
    f.write(r"\begin{aligned}" + "\n")
    f.write(fr"d\idx{0} \simeq {np.round(width, 2)}\," + r"{\si{\milli\meter}}." + r"\\" + "\n")
    f.write(r"\end{aligned}" + "\n")
    f.write(r"\end{equation*}" + "\n")
    f.close()



    
def generatetable(data ,name: string, cap: string, lab: string, titles: list):
    f = open("build/table" + name + ".tex", "w")
    
    f.write(r"\begin{table}" + "\n")
    f.write(r"\centering" + "\n")
    f.write(r"\caption{" + cap + r"}" + "\n")
    f.write(r"\label{tab:" + lab + r"}" + "\n")
    temp = "c"
    for i in range(1, len(titles)):
        temp += " c"
    f.write(r"\begin{tabular}[t]{" + temp + r"}" + "\n")
    f.write(r"\toprule" + "\n")
    temp = ""
    for i in titles:
        temp += i + " & "
    temp = temp[0:len(temp)-3]
    f.write(temp + r"\\" + "\n")
    f.write(r"\midrule" +"\n")
    for i in data:
        temp = ""
        for j in i:
            temp += str(j) + " & "
        temp = temp[0:len(temp)-3]
        f.write(temp + r"\\"+"\n")
    
    f.write(r"\bottomrule" + "\n")
    f.write(r"\end{tabular}" + "\n")
    f.write(r"\end{table}")
    f.close()

data = np.loadtxt("build/Scan_2_Z.txt")

x = data[:,0]
y = data[:,1]

data = np.array([[data[i][0], int(data[i][1]), data[i+len(data)//2][0], int(data[i+len(data)//2][1])] for i in range(len(data)//2)])
generatetable(data, 'zScan', 'Messdaten zum z-scan','zScan', [r'$z/mm$', 'counts',r'$z/mm$', 'counts'])
generateplot(x, y, r'$z$ in $mm$', 'counts', 'zScan', False)