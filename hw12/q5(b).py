import numpy as np
import matplotlib.pyplot as plt
import tqdm

sample_size = 1000000

# Exponential Distribution 
def exponential_inverse(x): # the inverse of the exponential distribution
    return -np.log(1 - x)

def inverse_transform_sampling(sample_size): # inverse transform sampling
    u = np.random.uniform(0, 1, sample_size) # uniform random numbers
    return exponential_inverse(u)

# Y ~ Expo(1)
Y = inverse_transform_sampling(sample_size) # sample points using inverse transform sampling
FoverG = np.exp(- 1 / 2 * ((Y - 1) ** 2))
Z = np.zeros(sample_size)
U = np.random.uniform(0, 1, len(Z))

for i in tqdm.tqdm(range(sample_size)):
    if FoverG[i] >= U[i]:
        Z[i] = Y[i]
    else:
        while True:
            y = inverse_transform_sampling(1)
            foverg = np.exp(- 1 / 2 * ((y - 1) ** 2))
            if np.random.uniform(0, 1) <= foverg:
                Z[i] = y
                break
            
U = np.random.uniform(0, 1, len(Z))
# if U > 1/2, then X = Z
# else X = -Z
X = np.where(U > 1 / 2, Z, -Z)

plt.hist(X, bins=100, density=True) # histogram of X

# N(0,1) PDF
def normal(x): # the PDF of N(0,1)
    return np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)

# theoretical PDF
x = np.linspace(-5, 5, 1000) # sample points for plotting pdf
pdf = normal(x) # pdf values at sample points
plt.plot(x, pdf)

plt.xlabel('x')
plt.ylabel('PDF')
plt.title('N(0,1)')
plt.legend(['theoretical PDF','histogram'])
plt.xticks(np.arange(-5,6))
plt.show()