import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import multivariate_normal

# Example parameters of multivariate
mu = np.array([0.5,0.5])
sig = np.array([[0.06,0.055],[0.055,0.06]])

# Create grid and multivariate normal
x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)
X, Y = np.meshgrid(x,y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X; pos[:, :, 1] = Y
p = multivariate_normal(mu, sig)


def banana_pdf(pos, p):
    """
    x, x**2 + y
    """
    n1, n2, _ = pos.shape
    pos = pos.reshape(-1,2)
    pos = np.vstack((pos[:,0],pos[:,0]**2 + pos[:,1])).T
    return p.pdf(pos).reshape((n1,n2))



plt.figure()
plt.contour(X,Y, banana_pdf(pos, p), cmap='magma')


# Experiment to have a fake sampling using only the posterior value
mask = (banana_pdf(pos, p) > 0.1 - np.random.normal(loc=0, scale=0.2))
pos = pos[mask]

plt.figure()
plt.scatter(pos[:, 0], pos[:, 1])

plt.show()

