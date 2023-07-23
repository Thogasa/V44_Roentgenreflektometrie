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
    return -int(np.floor(np.log10(np.abs(x)))) +1

def generateplot(x,y,func,  xlabel:string, ylabel:string, name: string, islog: bool, paramNames, units):
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.rcParams['font.size'] = 16
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['text.usetex'] = 1
    

    x_plot = np.linspace(x[0], np.max(x), 150)
    params, covariance_matrix = curve_fit(func, x, y)
    uncertainties = np.sqrt(np.diag(covariance_matrix))
    
    plt.plot(x,y,'o', color = "green",label ="Messdaten")    
    
    plt.plot(x_plot, func(x_plot, params[0],params[1], params[2]), color = "green", label = "Angenäherte Kurve")
    


    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(islog):
        plt.yscale('log')
    plt.legend(loc='best')
    plt.grid(True)
    
    plt.savefig("build/plot" + name + ".pdf")
    plt.clf()

    params[0] /= 100_000
    uncertainties[0] /= 100_000
    params[2] *= 1000
    uncertainties[2] *=1000
    sig = ufloat(params[2], uncertainties[2])/1000

    FWHM = 2*np.sqrt(np.log(2)*2)*sig
    print(params)


    f = open("build/params" + name + ".tex","w")
    f.write(r"\begin{equation*}" + "\n")
    f.write(r"\begin{aligned}" + "\n")
    for p, i in zip(paramNames, range(len(paramNames))):
        f.write(fr"{p} &= (" + str(np.round(params[i], sigFig(uncertainties[i]))) + r"\pm" + str(np.round(uncertainties[i], sigFig(uncertainties[i])))+ r")\," + f"{units[i]}" + r"\\" + "\n")
    f.write(fr"FWHM &= (" + str(np.round(FWHM.nominal_value, sigFig(FWHM.std_dev))) + r"\pm" + str(np.round(FWHM.std_dev, sigFig(FWHM.std_dev)))+ r")\," + r"\si{\degree}" + r"\\" + "\n")
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

data = np.loadtxt("build/Scan_1_Detector.txt")

x = data[:,0]
y = data[:,1]

print(np.max(y))

data = np.array([[data[i][0], int(data[i][1]), data[i+len(data)//2][0], int(data[i+len(data)//2][1])] for i in range(len(data)//2)])
generatetable(data, 'decScan', 'Messdaten zum Detectorscan','decScan', [r'$\alpha/°$', 'counts',r'$\alpha/°$', 'counts'])
generateplot(x, y, gauss, r'$\alpha in °$', 'counts', 'decScan', False, ['I\idx{max}', r'\mu', r'\sigma'], ['\cdot 10^{5}', '°', '\cdot 10^{-3}°'])