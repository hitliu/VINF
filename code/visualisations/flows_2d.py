import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from parameters import SAMPLES_SAVES_EXTENSION, SAMPLES_SAVES_FOLDER


def show_samples(zk, z0, mu):
    z0 = z0.numpy()
    mu = mu.numpy().flatten()
    zk = zk.numpy()

    mask_tl = (z0[:, 0] <= mu[0]) & (z0[:, 1] >= mu[1])
    mask_tr = (z0[:, 0] >= mu[0]) & (z0[:, 1] >= mu[1])
    mask_bl = (z0[:, 0] <= mu[0]) & (z0[:, 1] <= mu[1])
    mask_br = (z0[:, 0] >= mu[0]) & (z0[:, 1] <= mu[1])

    alpha = 0.5

    plt.figure(figsize=(8, 8))
    plt.scatter(zk[mask_tl][:, 0], zk[mask_tl][:, 1], color='red', alpha=alpha)
    plt.scatter(zk[mask_tr][:, 0], zk[mask_tr][:, 1], color='blue', alpha=alpha)
    plt.scatter(zk[mask_bl][:, 0], zk[mask_bl][:, 1], color='green', alpha=alpha)
    plt.scatter(zk[mask_br][:, 0], zk[mask_br][:, 1], color='yellow', alpha=alpha)


def visualise(q, shape, target):
    z0, zk, ldj, mu, log_var = q(tf.zeros(shape))

    show_samples(z0, z0, mu)
    show_samples(zk, z0, mu)

    try:
        with open(f"{SAMPLES_SAVES_FOLDER}/{target}.{SAMPLES_SAVES_EXTENSION}", 'rb') as f:
            original_samples = np.load(f)
    except FileNotFoundError:
        original_samples = []

    plt.figure()
    plt.scatter(z0[:, 0], z0[:, 1], color='crimson', alpha=0.6, label=r'$q_{0}$')
    if len(original_samples) > 0:
        plt.scatter(original_samples[:, 0], original_samples[:, 1], color='gray', alpha=0.6, label='True Posterior')
    plt.scatter(zk[:, 0], zk[:, 1], color='springgreen', alpha=0.6, label=r'$q_{k}$')
    plt.legend()

    plt.show()
