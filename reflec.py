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
    return -int(np.floor(np.log10(np.abs(x)))) +1

def generateplot(x,y,  xlabel:string, ylabel:string, name: string, islog: bool,):
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
    
    minIdxs = [64,73,83,91,102,110]
    plt.plot(x[minIdxs[0]], yCor[minIdxs[0]], 'o', color='b', label='Minima')

    for idx in minIdxs[1:]:
        plt.plot(x[idx], yCor[idx], 'o', color='b')

    
    plt.plot(x, yCor, color = 'r', label='Geometriefaktor korrigierte Messdaten')
    plt.plot(x,y, color = "b",label ="Diffus korrigierte Messdaten")        
    plt.axvline(0.22, color = 'r', linestyle = 'dashdot', label = r'$\alpha_c$')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(islog):
        plt.yscale('log')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig("build/plot" + name + ".pdf")
    plt.clf()

    print(np.where(x==0.320))
    print(np.where(x==0.365))
    print(np.where(x==0.415))
    print(np.where(x==0.455))
    print(np.where(x==0.510))
    print(np.where(x==0.550))

    minIdxs = [64,73,83,91,102,110]
    dels = []
    for i in range(len(minIdxs[:len(minIdxs)-1])):
        dels.append(x[minIdxs[i+1]]-x[minIdxs[i]])

    print(dels)
    aveDel = ufloat(np.mean(dels), 1/len(dels)*np.sum((dels-np.mean(dels))**2))
    d = 1.541/2/(aveDel*np.pi/180)
    print(aveDel)
    print(d.nominal_value)

    f = open("build/erg" + name + ".tex","w")
    f.write(r"\begin{equation*}" + "\n")
    f.write(r"\begin{aligned}" + "\n")
    f.write(r"\Delta\alpha\idx{ave} &=" + "({:.6f}".format(np.round(aveDel.nominal_value, sigFig(aveDel.std_dev))) + r" \pm " + "{:.6f}".format(np.round(aveDel.std_dev, sigFig(aveDel.std_dev))) + r")\,{\si{\degree}}" + r"\\" + "\n")
    f.write(r"\d &=" + f"({np.round(d.nominal_value, sigFig(d.std_dev))}" + r" \pm " + f"{np.round(d.std_dev, sigFig(d.std_dev))}" + r")\cdot 10^{-10}\,{\si{\meter}}." + r"\\" + "\n")
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

data = np.loadtxt("build/Scan_6_Oszillation_bei_0.txt")
data1 = np.loadtxt("build/Scan_7_Oszillation_bei_0,1.txt")

data = np.array([[d[0], d[1]-d1[1]] for d, d1 in zip(data, data1)])

data = np.array([[d[0],d[1]*5/(9.7e5)] for d in data])

x = data[:,0]
y = data[:,1]



data = np.array([[data[i][0], int(data[i][1]), data[i+len(data)//2][0], int(data[i+len(data)//2][1])] for i in range(len(data)//2)])

generatetable(data, 'reflecScan', 'Messdaten der Reflektivitaet','reflecScan', [r'$\alpha/°$', 'counts',r'$\alpha/°$', 'counts'])
generateplot(x, y, r'$\alpha$ in $°$', 'Reflektivität', 'reflecScan', True)