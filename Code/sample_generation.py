"""
Scripts to generate data samples.
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import multivariate_normal
from serialization import serialize_object

def generate_spsd(n):
    m = np.random.uniform(0,2,size=n)
    m = m@(m.T)
    m = m + n*np.eye(n)
    return m

def multivariate_gaussian_2d(n_components, n_samples=100, span=[-10,10]):
    mus = []
    sigmas = []
    X = np.zeros(((n_samples*n_components),2))

    # Create grid for contours
    x_c = np.linspace(2*span[0],2*span[1],100)
    y_c = np.linspace(2*span[0],2*span[1],100)
    X_c, Y_c = np.meshgrid(x_c,y_c)
    pos = np.empty(X_c.shape + (2,))
    pos[:, :, 0] = X_c; pos[:, :, 1] = Y_c
    contours = {'X': X_c, 'Y': Y_c, 'c': []}

    for n in range(n_components):
        mus.append(np.random.uniform(span[0],span[1],size=(1,2))[0])
        sigmas.append(generate_spsd(2))
        X[n*n_samples:(n+1)*n_samples,:] = np.random.multivariate_normal(mus[-1],sigmas[-1], size=n_samples)
        contours['c'].append(multivariate_normal(mus[-1],sigmas[-1]).pdf(pos))
    return X, mus, sigmas, contours



X, mus, sigmas, contours = multivariate_gaussian_2d(8, n_samples=200)
SAVE_DATA_NAME = 'data/mvg2D_X.pickle'
SAVE_PARAMS_NAME = 'data/mvg2D_params.pickle'
SAVE_CONTOURS_NAME = 'data/mvg2D_contours.pickle'
serialize_object(X, SAVE_DATA_NAME)
serialize_object({'mus': mus, 'sigmas': sigmas}, SAVE_PARAMS_NAME)
serialize_object(contours, SAVE_CONTOURS_NAME)

# Visualization to check interest of samples.
plt.plot(X[:,0], X[:,1], 'o')
for contour in contours['c']:
    plt.contour(contours['X'], contours['Y'], contour)
plt.show()


