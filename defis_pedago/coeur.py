import numpy as np
import matplotlib.pyplot as plt

 
def coeur(x):
    y =  ((x**2)**(1/3)) + np.sqrt(1-(x**2)) 
    z =   - ((x**2)**(1/3)) + np.sqrt(1-(x**2))
    return y,z


x = np.linspace(-1,1, 1000)
H,B = coeur(x)

plt.plot(H, linewidth = 10,  color='red')
plt.plot(-B, linewidth = 10,  color='red')

plt.show()
