import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def parratt(a_i, del2, del3, sig1, sig2,b2,b3, d2):
    a_irad = np.deg2rad(a_i)

    # d2 =  1.675e-09
    # d2 = 8.6e-8

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


data = np.loadtxt("build/Scan_6_Oszillation_bei_0.txt")
data1 = np.loadtxt("build/Scan_7_Oszillation_bei_0,1.txt")

# data3 = np.array([[d[0],d[1]/(5*np.max(data[:,1]))] for d in data])


data = np.array([[d[0], d[1]-d1[1]] for d, d1 in zip(data, data1)])
# data = np.array([[d[0],d[1]*5/(9.7e5)] for d in data])

x = data[:,0]
y = data[:,1]


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
        

    


# Define initial parameters
del2 = 7.6e-06
del3 = 3.5e-6
sig1 = 5.5e-10
sig2 = 6.5e-10
b2 = 3e-9
b3 = 1.5e-7
d2 =  1.675e-09

del2 = 7.6e-06
del3 = 8.077e-6
sig1 = 2.688e-9
sig2 = 4.829e-10
b2 = 3.863e-7
b3 = 1.483e-5
d2 =  8.139e-08

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(x, parratt(x, del2, del3, sig1, sig2, b2, b3, d2), lw=2)
ax.plot(x, yCor, color = 'r')

ax.set_yscale('log')
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.1, bottom=0.4)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.05, 0.65, 0.03])
del2slider = Slider(
    ax=axfreq,
    label='del2',
    valmin=1e-6,
    valmax=1e-4,
    valinit=del2,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.25, 0.1, 0.65, 0.03])
del3slider = Slider(
    ax=axamp,
    label="del3",
    valmin=1e-8,
    valmax=1e-5,
    valinit=del3
)
# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.15, 0.65, 0.03])
sig1slider = Slider(
    ax=axfreq,
    label='sig1',
    valmin=1e-10,
    valmax=1e-8,
    valinit=sig1,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.25, 0.2, 0.65, 0.03])
sig2slider = Slider(
    ax=axamp,
    label="sig2",
    valmin=1e-14,
    valmax=1e-9,
    valinit=sig2
)
# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.25, 0.65, 0.03])
b2slider = Slider(
    ax=axfreq,
    label='b2',
    valmin=1e-10,
    valmax=1e-6,
    valinit=b2,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.25, 0.3, 0.65, 0.03])
b3slider = Slider(
    ax=axamp,
    label="b3",
    valmin=1e-8,
    valmax=1e-4,
    valinit=b3
)
axamp = fig.add_axes([0.25, 0.35, 0.65, 0.03])
d2slider = Slider(
    ax=axamp,
    label="d2",
    valmin=6e-8,
    valmax=1e-7,
    valinit=d2
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(parratt(x, del2slider.val, del3slider.val, sig1slider.val, sig2slider.val, b2slider.val, b3slider.val, d2slider.val))
    print(del2slider.val, del3slider.val, sig1slider.val, sig2slider.val, b2slider.val, b3slider.val, d2slider.val)
    fig.canvas.draw_idle()


# register the update function with each slider
del2slider.on_changed(update)
del3slider.on_changed(update)
sig1slider.on_changed(update)
sig2slider.on_changed(update)
b2slider.on_changed(update)
b3slider.on_changed(update)
d2slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    del2slider.reset()
    del3slider.reset()
    sig1slider.reset()
    sig2slider.reset()
button.on_clicked(reset)


plt.show()